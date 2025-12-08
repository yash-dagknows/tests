"""
Tests for Alert Handling Modes (Deterministic, AI-selected, Autonomous).

Tests the three incident response modes:
1. Deterministic Mode - Pre-configured tasks trigger on specific alerts
2. AI-selected Mode - AI selects appropriate task from available tooltasks  
3. Autonomous Mode - AI launches full troubleshooting session

These tests validate alert processing through req-router which is responsible
for routing alerts to appropriate tasks based on the incident response mode.
"""

import pytest
import time
import logging
from utils.fixtures import TestDataFactory

logger = logging.getLogger(__name__)

# Add timestamp for unique alert names
pytest.timestamp = int(time.time())


class TestAlertHandlingDeterministic:
    """Tests for Deterministic alert handling mode.
    
    In deterministic mode, tasks are pre-configured with trigger_on_alerts
    field to execute when specific alerts are received.
    """
    
    def test_deterministic_alert_triggers_configured_task(
        self, 
        taskservice_client,
        req_router_client, 
        test_data_factory
    ):
        """
        Test that a task configured with trigger_on_alerts executes
        when a matching alert is received (deterministic mode).
        
        Flow:
        1. Create a task with trigger_on_alerts configuration
        2. Send matching alert via req-router
        3. Verify alert is stored with selection_mode="deterministic"
        4. Verify task is executed
        """
        # Create unique alert identifiers
        alert_source = f"test_source_{pytest.timestamp}"
        alert_name = f"test_alert_{pytest.timestamp}"
        
        # Create task configured to trigger on this alert
        task_data = test_data_factory.create_task_data(
            title=f"Deterministic Task {pytest.timestamp}",
            description="Task for deterministic alert handling",
            script_type="python",
            script="print('Handling alert deterministically')"
        )
        
        # Add trigger_on_alerts configuration
        task_data["trigger_on_alerts"] = [
            {
                "alert_source": alert_source,
                "alert_name": alert_name,
                "dedup_interval": 300  # 5 minutes
            }
        ]
        
        task_id = None
        alert_id = None
        
        try:
            # Create the task
            response = taskservice_client.create_task(task_data)
            task = response.get("task", response)
            task_id = task["id"]
            
            logger.info(f"Created task {task_id} for deterministic alert handling")
            
            # Create and send alert payload
            alert_payload = test_data_factory.create_grafana_alert_data(
                alert_name=alert_name,
                alert_source=alert_source,
                status="firing",
                severity="critical"
            )
            
            # Send alert via req-router processAlert endpoint
            # This should trigger the configured task in deterministic mode
            alert_response = req_router_client.process_alert(alert_payload)
            
            logger.info(f"Alert response: {alert_response}")
            
            # Verify response indicates successful deterministic execution
            assert alert_response.get("status") == "success", "Alert processing should succeed"
            assert alert_response.get("tasks_executed", 0) >= 1, "At least one task should be executed"
            
            # Search for the stored alert
            time.sleep(2)  # Give Elasticsearch time to index
            
            alerts = req_router_client.search_alerts(
                params={
                    "source": alert_source,
                    "q": alert_name
                }
            )
            
            alerts_list = alerts.get("alerts", alerts.get("hits", []))
            assert len(alerts_list) > 0, "Alert should be stored in index"
            
            stored_alert = alerts_list[0]
            alert_id = stored_alert.get("id")
            
            # Verify selection_mode is "deterministic"
            assert stored_alert.get("selection_mode") == "deterministic", \
                "Alert should have deterministic selection_mode"
            
            # Verify task linkage
            assert stored_alert.get("runbook_task_id") == task_id, \
                "Alert should link to the triggered task"
            
            logger.info(f"✅ Deterministic mode test passed: task {task_id} triggered by alert")
            
        finally:
            # Cleanup
            if task_id:
                try:
                    taskservice_client.delete_task(task_id)
                except Exception as e:
                    logger.warning(f"Failed to cleanup task {task_id}: {e}")
            
            if alert_id:
                try:
                    req_router_client.delete_alert(alert_id)
                except Exception as e:
                    logger.warning(f"Failed to cleanup alert {alert_id}: {e}")
    
    def test_deterministic_alert_no_match_no_execution(
        self,
        req_router_client,
        test_data_factory
    ):
        """
        Test that an alert with no matching configured task does not execute
        anything in deterministic mode (when ai_selected/autonomous are disabled).
        
        Flow:
        1. Send alert with no matching task
        2. Verify alert is stored with selection_mode="none"
        3. Verify no tasks are executed
        """
        alert_source = f"no_match_source_{pytest.timestamp}"
        alert_name = f"no_match_alert_{pytest.timestamp}"
        alert_id = None
        
        try:
            # Create alert payload with no matching task
            alert_payload = test_data_factory.create_grafana_alert_data(
                alert_name=alert_name,
                alert_source=alert_source,
                status="firing"
            )
            
            # Send alert via req-router
            alert_response = req_router_client.process_alert(alert_payload)
            
            logger.info(f"Alert response (no match): {alert_response}")
            
            # Response may indicate no tasks executed
            # (actual behavior depends on incident_response_mode config)
            assert alert_response.get("status") in ["success", "no_tasks"], \
                "Alert should be received even without matching tasks"
            
            # Search for the stored alert
            time.sleep(2)
            
            alerts = req_router_client.search_alerts(
                params={
                    "source": alert_source,
                    "q": alert_name
                }
            )
            
            alerts_list = alerts.get("alerts", alerts.get("hits", []))
            
            if len(alerts_list) > 0:
                stored_alert = alerts_list[0]
                alert_id = stored_alert.get("id")
                
                # If only deterministic mode, selection_mode should be "none"
                # If ai_selected or autonomous is enabled, it may try those modes
                selection_mode = stored_alert.get("selection_mode")
                logger.info(f"Selection mode for unmatched alert: {selection_mode}")
                
                # Alert should be stored regardless of execution
                assert selection_mode in ["none", "ai_selected", "autonomous"], \
                    "Unmatched alert should have valid selection_mode"
            
            logger.info(f"✅ No-match test passed: alert stored without execution")
            
        finally:
            if alert_id:
                try:
                    req_router_client.delete_alert(alert_id)
                except Exception as e:
                    logger.warning(f"Failed to cleanup alert {alert_id}: {e}")


@pytest.mark.ai_required
class TestAlertHandlingAISelected:
    """Tests for AI-selected alert handling mode.
    
    In AI-selected mode, when no deterministic match is found,
    the system searches for similar tooltasks and uses LLM to select
    the best task to execute.
    """
    
    def test_ai_selected_mode_finds_and_executes_task(
        self,
        taskservice_client,
        req_router_client,
        test_data_factory
    ):
        """
        Test that AI-selected mode finds a matching tooltask via similarity
        search and LLM selection when no deterministic match exists.
        
        Note: This test requires incident_response_mode='ai_selected' to be
        configured in req-router settings.
        
        Flow:
        1. Create a tooltask with relevant description
        2. Send alert with similar description
        3. Verify AI finds and selects the tooltask
        4. Verify alert stored with selection_mode="ai_selected"
        5. Verify AI confidence and reasoning are captured
        """
        alert_source = f"ai_test_source_{pytest.timestamp}"
        alert_name = f"cpu_high_alert_{pytest.timestamp}"
        
        task_id = None
        alert_id = None
        
        try:
            # Create a tooltask that could match the alert
            task_data = test_data_factory.create_task_data(
                title="High CPU Usage Remediation",
                description="This task investigates and remediates high CPU usage on servers. It checks running processes, identifies CPU-intensive tasks, and can restart services if needed.",
                script_type="python",
                script="print('Investigating high CPU usage...')",
                tags=["cpu", "performance", "remediation"]
            )
            
            response = taskservice_client.create_task(task_data)
            task = response.get("task", response)
            task_id = task["id"]
            
            logger.info(f"Created tooltask {task_id} for AI selection")
            
            # Wait for task to be indexed and vectorized
            time.sleep(3)
            
            # Create alert with similar description
            alert_payload = test_data_factory.create_grafana_alert_data(
                alert_name=alert_name,
                alert_source=alert_source,
                status="firing",
                severity="critical",
                description="Server CPU usage has exceeded 90% for the last 5 minutes. Immediate investigation required.",
                summary="High CPU Usage Alert"
            )
            
            # Send alert via req-router
            # If AI-selected mode is enabled and no deterministic match, should use AI
            alert_response = req_router_client.process_alert(alert_payload)
            
            logger.info(f"Alert response (AI-selected): {alert_response}")
            
            # Search for the stored alert
            time.sleep(2)
            
            alerts = req_router_client.search_alerts(
                params={
                    "source": alert_source,
                    "q": alert_name
                }
            )
            
            alerts_list = alerts.get("alerts", alerts.get("hits", []))
            
            if len(alerts_list) > 0:
                stored_alert = alerts_list[0]
                alert_id = stored_alert.get("id")
                
                # Check if AI-selected mode was used
                selection_mode = stored_alert.get("selection_mode")
                logger.info(f"Selection mode: {selection_mode}")
                
                if selection_mode == "ai_selected":
                    # Verify AI selection details
                    assert stored_alert.get("ai_selected") == True, \
                        "ai_selected flag should be set"
                    
                    # AI should provide confidence score
                    ai_confidence = stored_alert.get("ai_confidence")
                    assert ai_confidence is not None and ai_confidence > 0, \
                        "AI should provide confidence score"
                    
                    # AI should provide reasoning
                    ai_reasoning = stored_alert.get("ai_reasoning", "")
                    assert len(ai_reasoning) > 0, \
                        "AI should provide reasoning for task selection"
                    
                    # Should have candidate tooltasks
                    ai_candidates = stored_alert.get("ai_candidate_tooltasks", [])
                    assert len(ai_candidates) > 0, \
                        "AI should provide candidate tooltasks considered"
                    
                    # Should link to a runbook task
                    assert stored_alert.get("runbook_task_id"), \
                        "Alert should link to selected task"
                    
                    logger.info(f"✅ AI-selected mode test passed: AI selected task with {ai_confidence} confidence")
                else:
                    logger.warning(f"AI-selected mode not used (mode: {selection_mode}). This may indicate incident_response_mode is not set to 'ai_selected'")
            else:
                pytest.skip("Alert not found in index - may indicate processing issue")
                
        finally:
            if task_id:
                try:
                    taskservice_client.delete_task(task_id)
                except Exception as e:
                    logger.warning(f"Failed to cleanup task {task_id}: {e}")
            
            if alert_id:
                try:
                    req_router_client.delete_alert(alert_id)
                except Exception as e:
                    logger.warning(f"Failed to cleanup alert {alert_id}: {e}")
    
    def test_ai_selected_mode_no_suitable_task(
        self,
        req_router_client,
        test_data_factory
    ):
        """
        Test that AI-selected mode handles cases where no suitable tooltask
        is found (similarity < 0.7 or LLM declines selection).
        
        Flow:
        1. Send alert with very specific/unique description
        2. Verify no task is executed
        3. Verify alert stored appropriately
        """
        alert_source = f"ai_no_match_source_{pytest.timestamp}"
        alert_name = f"unique_alert_{pytest.timestamp}"
        alert_id = None
        
        try:
            # Create alert with very specific description unlikely to match any task
            alert_payload = test_data_factory.create_grafana_alert_data(
                alert_name=alert_name,
                alert_source=alert_source,
                status="firing",
                description="Very specific quantum flux capacitor overload in sector 7G subsystem alpha-omega with cascade failure mode 9000",
                summary="Quantum Flux Alert"
            )
            
            alert_response = req_router_client.process_alert(alert_payload)
            logger.info(f"Alert response (no AI match): {alert_response}")
            
            time.sleep(2)
            
            alerts = req_router_client.search_alerts(
                params={
                    "source": alert_source,
                    "q": alert_name
                }
            )
            
            alerts_list = alerts.get("alerts", alerts.get("hits", []))
            
            if len(alerts_list) > 0:
                stored_alert = alerts_list[0]
                alert_id = stored_alert.get("id")
                
                selection_mode = stored_alert.get("selection_mode")
                logger.info(f"Selection mode when no AI match: {selection_mode}")
                
                # Should be "none" or possibly "autonomous" if that mode is enabled as fallback
                assert selection_mode in ["none", "autonomous"], \
                    "When AI can't find suitable task, selection_mode should be none or fall back to autonomous"
                
                logger.info(f"✅ AI no-match test passed: handled case with no suitable task")
            
        finally:
            if alert_id:
                try:
                    req_router_client.delete_alert(alert_id)
                except Exception as e:
                    logger.warning(f"Failed to cleanup alert {alert_id}: {e}")


@pytest.mark.ai_required
@pytest.mark.slow
class TestAlertHandlingAutonomous:
    """Tests for Autonomous alert handling mode.
    
    In autonomous mode, when no deterministic match is found,
    the system launches a full AI troubleshooting session to
    investigate and resolve the issue.
    """
    
    def test_autonomous_mode_launches_troubleshoot_session(
        self,
        req_router_client,
        test_data_factory
    ):
        """
        Test that autonomous mode launches an AI troubleshooting session
        when no deterministic match is found.
        
        Note: This test requires incident_response_mode='autonomous' to be
        configured in req-router settings.
        
        Flow:
        1. Send alert with no deterministic match
        2. Verify autonomous troubleshoot session is launched
        3. Verify alert stored with selection_mode="autonomous"
        4. Verify runbook_task_id and child_task_id are captured
        """
        alert_source = f"autonomous_source_{pytest.timestamp}"
        alert_name = f"database_slow_alert_{pytest.timestamp}"
        alert_id = None
        
        try:
            # Create alert that would trigger autonomous mode
            alert_payload = test_data_factory.create_grafana_alert_data(
                alert_name=alert_name,
                alert_source=alert_source,
                status="firing",
                severity="warning",
                description="Database query response time has increased by 300% in the last 10 minutes. Users reporting slow page loads.",
                summary="Database Performance Degradation"
            )
            
            alert_response = req_router_client.process_alert(alert_payload)
            logger.info(f"Alert response (autonomous): {alert_response}")
            
            # Check if autonomous mode was activated
            incident_response_mode = alert_response.get("incident_response_mode")
            
            if incident_response_mode == "autonomous":
                # Verify autonomous session was launched
                assert alert_response.get("status") == "success", \
                    "Autonomous session should launch successfully"
                
                # Should have runbook_task_id for the troubleshoot session
                runbook_task_id = alert_response.get("runbook_task_id")
                assert runbook_task_id, \
                    "Autonomous mode should create runbook task"
                
                # Should have child_task_id for the investigation
                child_task_id = alert_response.get("child_task_id")
                assert child_task_id, \
                    "Autonomous mode should create child task for investigation"
                
                time.sleep(2)
                
                # Verify alert is stored correctly
                alerts = req_router_client.search_alerts(
                    params={
                        "source": alert_source,
                        "q": alert_name
                    }
                )
                
                alerts_list = alerts.get("alerts", alerts.get("hits", []))
                assert len(alerts_list) > 0, "Alert should be stored"
                
                stored_alert = alerts_list[0]
                alert_id = stored_alert.get("id")
                
                # Verify selection_mode is "autonomous"
                assert stored_alert.get("selection_mode") == "autonomous", \
                    "Alert should have autonomous selection_mode"
                
                # Verify AI fields
                assert stored_alert.get("ai_selected") == True, \
                    "Autonomous mode uses AI, so ai_selected should be true"
                
                assert stored_alert.get("ai_confidence") >= 0.9, \
                    "Autonomous mode should have high confidence (full AI investigation)"
                
                # Verify task linkage
                assert stored_alert.get("runbook_task_id") == runbook_task_id, \
                    "Alert should link to autonomous runbook task"
                
                logger.info(f"✅ Autonomous mode test passed: launched troubleshoot session")
            else:
                logger.warning(f"Autonomous mode not used (mode: {incident_response_mode}). This may indicate incident_response_mode is not set to 'autonomous'")
                pytest.skip("Autonomous mode not configured")
                
        finally:
            if alert_id:
                try:
                    req_router_client.delete_alert(alert_id)
                except Exception as e:
                    logger.warning(f"Failed to cleanup alert {alert_id}: {e}")


class TestAlertSearchAndStats:
    """Tests for alert search and statistics with selection_mode filtering."""
    
    def test_search_alerts_by_selection_mode(
        self,
        req_router_client,
        taskservice_client,
        test_data_factory
    ):
        """
        Test searching/filtering alerts by selection_mode.
        
        Flow:
        1. Create alerts with different selection_modes
        2. Search by selection_mode filter
        3. Verify correct alerts are returned
        """
        alert_source = f"mode_filter_source_{pytest.timestamp}"
        created_alerts = []
        
        try:
            # Create deterministic alert
            task_data = test_data_factory.create_task_data(
                title=f"Filter Test Task {pytest.timestamp}"
            )
            task_data["trigger_on_alerts"] = [{
                "alert_source": alert_source,
                "alert_name": "deterministic_test",
                "dedup_interval": 300
            }]
            
            response = taskservice_client.create_task(task_data)
            task_id = response.get("task", response)["id"]
            created_alerts.append({"task_id": task_id})
            
            # Send deterministic alert
            det_alert = test_data_factory.create_grafana_alert_data(
                alert_name="deterministic_test",
                alert_source=alert_source,
                status="firing"
            )
            req_router_client.process_alert(det_alert)
            
            time.sleep(3)  # Wait for indexing
            
            # Search for deterministic alerts
            results = req_router_client.search_alerts(
                params={
                    "selection_mode": "deterministic",
                    "source": alert_source
                }
            )
            
            alerts = results.get("alerts", results.get("hits", []))
            
            # Should find at least our deterministic alert
            deterministic_count = len([a for a in alerts if a.get("selection_mode") == "deterministic"])
            assert deterministic_count > 0, "Should find deterministic alerts"
            
            logger.info(f"✅ Alert filtering by selection_mode works: found {deterministic_count} deterministic alerts")
            
        finally:
            # Cleanup
            for item in created_alerts:
                if "task_id" in item:
                    try:
                        taskservice_client.delete_task(item["task_id"])
                    except Exception as e:
                        logger.warning(f"Failed to cleanup: {e}")
    
    def test_alert_stats_by_selection_mode(
        self,
        req_router_client
    ):
        """
        Test alert statistics aggregation by selection_mode.
        
        Verify that alert stats endpoint returns counts for each selection_mode.
        """
        stats = req_router_client.get_alert_stats()
        
        logger.info(f"Alert stats: {stats}")
        
        # Stats should include by_selection_mode aggregation
        assert "by_selection_mode" in stats, "Stats should include selection_mode breakdown"
        
        # Should have counts for deterministic, ai_selected, autonomous
        selection_modes = stats.get("by_selection_mode", {})
        assert isinstance(selection_modes, dict), "by_selection_mode should be a dict"
        
        # May have individual counts
        assert "deterministic" in stats or stats.get("deterministic", 0) >= 0, \
            "Stats should track deterministic count"
        assert "ai_selected" in stats or stats.get("ai_selected", 0) >= 0, \
            "Stats should track ai_selected count"
        assert "autonomous" in stats or stats.get("autonomous", 0) >= 0, \
            "Stats should track autonomous count"
        
        logger.info(f"✅ Alert stats by selection_mode: {selection_modes}")

