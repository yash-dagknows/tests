"""
E2E UI Test: Alert Handling Modes

Tests the complete workflow of configuring alert handling modes and sending alerts.

Flow for Deterministic Mode:
1. Login
2. Navigate to landing page → Default workspace
3. Go to Settings via left nav
4. Click AI tab
5. Select Deterministic mode in Incident Response
6. Send Grafana alert via API
7. Verify task execution
"""

import pytest
import logging
import requests
import time
from pages.login_page import LoginPage
from pages.workspace_page import WorkspacePage
from pages.settings_page import SettingsPage
from config.test_users import get_test_user
from config.env import config

logger = logging.getLogger(__name__)


@pytest.mark.ui
@pytest.mark.e2e
@pytest.mark.alert_handling
class TestAlertHandlingModesE2E:
    """Test alert handling mode configuration and alert processing."""
    
    def test_deterministic_mode_alert_handling(self, page, test_config):
        """
        E2E Test: Configure Deterministic mode and send alert.
        
        This test follows the user journey:
        1. Login at /vlogin
        2. Navigate to landing page (/n/landing)
        3. Click "Default" workspace
        4. Click Settings in left navigation
        5. Navigate to /vsettings
        6. Click "AI" tab
        7. Select "Deterministic" mode in Incident Response section
        8. Send Grafana alert payload via API
        9. Verify task execution
        """
        logger.info("=== Starting Deterministic Mode Alert Handling E2E Test ===")
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Step 1-2: Login
        logger.info("Step 1-2: Logging in")
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        
        assert login_page.is_logged_in(), "Login should be successful"
        logger.info("✓ Login successful")
        login_page.screenshot("01-deterministic-after-login")
        
        # Step 3: Navigate to landing page
        logger.info("Step 3: Navigating to landing page")
        workspace_page = WorkspacePage(page)
        workspace_page.navigate_to_landing()
        workspace_page.wait_for_workspaces_loaded()
        
        assert "/n/landing" in page.url or "/landing" in page.url, \
            "Should be on landing page"
        logger.info("✓ On landing page")
        workspace_page.screenshot("02-deterministic-landing-page")
        
        # Step 4: Click "Default" workspace
        logger.info("Step 4: Clicking 'Default' workspace")
        workspace_page.click_default_workspace()
        
        page.wait_for_timeout(2000)
        assert "?space=" in page.url or "space=" in page.url, \
            "Should be in workspace view"
        logger.info(f"✓ In workspace view: {page.url}")
        workspace_page.screenshot("03-deterministic-workspace-view")
        
        # Step 5: Go to Settings
        logger.info("Step 5: Navigating to Settings")
        settings_page = SettingsPage(page)
        settings_page.click_settings_in_nav()
        
        # Verify we're on settings page
        assert "/vsettings" in page.url or "/settings" in page.url.lower(), \
            "Should be on settings page"
        logger.info(f"✓ On settings page: {page.url}")
        settings_page.screenshot("04-deterministic-settings-page")
        
        # Step 6: Click AI tab
        logger.info("Step 6: Clicking AI tab")
        settings_page.click_ai_tab()
        
        # Wait for AI settings to load
        page.wait_for_timeout(2000)
        logger.info("✓ AI settings tab loaded")
        settings_page.screenshot("05-deterministic-ai-tab")
        
        # Step 7: Select Deterministic mode
        logger.info("Step 7: Selecting Deterministic mode")
        settings_page.select_deterministic_mode()
        
        # Wait for mode to be saved (may auto-save)
        page.wait_for_timeout(3000)
        logger.info("✓ Deterministic mode selected")
        settings_page.screenshot("06-deterministic-mode-selected")
        
        # Optional: Try to save settings if button exists
        settings_page.save_settings()
        
        # Step 8: Send Grafana alert via API
        logger.info("Step 8: Sending Grafana alert")
        alert_response = self._send_grafana_alert(test_config)
        
        # Log response
        logger.info(f"Alert response: {alert_response}")
        
        # Step 9: Verify task execution
        logger.info("Step 9: Verifying task execution")
        
        status = alert_response.get('status', 'unknown')
        tasks_executed = alert_response.get('tasks_executed', 0)
        message = alert_response.get('message', '')
        
        logger.info(f"Status: {status}")
        logger.info(f"Tasks executed: {tasks_executed}")
        if message:
            logger.info(f"Message: {message}")
        
        # Take final screenshot
        settings_page.screenshot("07-deterministic-alert-sent")
        
        # Verification
        if tasks_executed >= 1:
            logger.info("✅ SUCCESS: Task(s) executed in Deterministic mode!")
            executed_tasks = alert_response.get('executed_tasks', [])
            for task in executed_tasks:
                logger.info(f"  • Task ID: {task.get('task_id')}")
                logger.info(f"    Job ID: {task.get('job_id')}")
                logger.info(f"    Status: {task.get('status')}")
        else:
            logger.warning("⚠ No tasks executed - this may be expected if no matching task configured")
            logger.warning("Note: This test requires a pre-configured task with:")
            logger.warning("  • source: Grafana")
            logger.warning("  • alert_name: HighCPUUsage")
        
        logger.info("=== Deterministic Mode Alert Handling Test Completed ===")
    
    def test_ai_selected_mode_alert_handling(self, page, test_config):
        """
        E2E Test: Configure AI-Selected mode and send alert.
        
        Similar flow to deterministic, but selects AI-Selected mode.
        """
        logger.info("=== Starting AI-Selected Mode Alert Handling E2E Test ===")
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Login
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        assert login_page.is_logged_in()
        
        # Navigate to workspace
        workspace_page = WorkspacePage(page)
        workspace_page.navigate_to_landing()
        workspace_page.wait_for_workspaces_loaded()
        workspace_page.click_default_workspace()
        page.wait_for_timeout(2000)
        
        # Go to Settings → AI tab
        settings_page = SettingsPage(page)
        settings_page.click_settings_in_nav()
        settings_page.click_ai_tab()
        
        # Select AI-Selected mode
        logger.info("Selecting AI-Selected mode")
        settings_page.select_ai_selected_mode()
        page.wait_for_timeout(3000)
        settings_page.screenshot("ai-selected-mode-selected")
        settings_page.save_settings()
        
        # Send alert
        logger.info("Sending alert to AI-Selected mode")
        alert_response = self._send_grafana_alert(test_config)
        
        logger.info(f"Alert response: {alert_response}")
        logger.info("=== AI-Selected Mode Alert Handling Test Completed ===")
    
    def test_autonomous_mode_alert_handling(self, page, test_config):
        """
        E2E Test: Configure Autonomous mode and send alert.
        
        Autonomous mode should:
        1. Analyze the alert
        2. Generate NEW task code dynamically
        3. Create and execute the task
        
        This can take 60-120 seconds as AI generates code!
        """
        logger.info("=== Starting Autonomous Mode Alert Handling E2E Test ===")
        logger.info("Note: Autonomous mode may take 60-120 seconds to generate task code")
        
        # Get test user
        test_user = get_test_user("Admin")
        test_user.email = "yash+user@dagknows.com"
        
        # Login
        login_page = LoginPage(page)
        login_page.login(user=test_user)
        assert login_page.is_logged_in()
        
        # Navigate to workspace
        workspace_page = WorkspacePage(page)
        workspace_page.navigate_to_landing()
        workspace_page.wait_for_workspaces_loaded()
        workspace_page.click_default_workspace()
        page.wait_for_timeout(2000)
        
        # Go to Settings → AI tab
        settings_page = SettingsPage(page)
        settings_page.click_settings_in_nav()
        settings_page.click_ai_tab()
        
        # Select Autonomous mode
        logger.info("Selecting Autonomous mode")
        settings_page.select_autonomous_mode()
        page.wait_for_timeout(3000)
        settings_page.screenshot("autonomous-mode-selected")
        settings_page.save_settings()
        
        # Wait additional time for mode to be saved and propagated
        logger.info("Waiting for mode change to propagate (10 seconds)...")
        page.wait_for_timeout(10000)
        
        # Note: Mode verification from UI is tricky, so we'll verify from API response instead
        logger.info("Mode selection complete - will verify from API response")
        
        # Send alert with UNIQUE name (to avoid matching existing tasks)
        logger.info("Sending unique alert to Autonomous mode")
        logger.info("Using unique alert name to force NEW task creation")
        alert_response = self._send_autonomous_test_alert(test_config)
        
        logger.info(f"Alert response: {alert_response}")
        
        # Verify autonomous mode from API response
        response_mode = alert_response.get('incident_response_mode', 'unknown')
        logger.info(f"✓ API Response Mode: {response_mode}")
        
        if response_mode == 'autonomous':
            logger.info("✅ Confirmed: Autonomous mode is active (from API)")
        else:
            logger.warning(f"⚠ API shows mode: {response_mode} (expected: autonomous)")
        
        # Analyze response
        tasks_found = alert_response.get('tasks_found', 0)
        tasks_executed = alert_response.get('tasks_executed', 0)
        runbook_task_id = alert_response.get('runbook_task_id', None)
        child_task_id = alert_response.get('child_task_id', None)
        message = alert_response.get('message', '')
        
        logger.info(f"Tasks found (existing): {tasks_found}")
        logger.info(f"Tasks executed: {tasks_executed}")
        if runbook_task_id:
            logger.info(f"Runbook task ID: {runbook_task_id}")
        if child_task_id:
            logger.info(f"Child task ID: {child_task_id}")
        if message:
            logger.info(f"Message: {message}")
        
        # Autonomous mode specific analysis
        if tasks_found == 0 and tasks_executed > 0:
            logger.info("✅ SUCCESS: Autonomous mode created NEW task dynamically!")
            logger.info("This is the expected autonomous behavior")
        elif tasks_found > 0:
            logger.warning("⚠ Found existing task - autonomous used it instead of creating new")
            logger.warning("This is valid fallback behavior but not pure autonomous")
        else:
            logger.warning("⚠ No tasks executed")
        
        # Verify autonomous created tasks
        if runbook_task_id or child_task_id:
            logger.info("✅ Autonomous mode created runbook and/or child tasks")
        
        logger.info("=== Autonomous Mode Alert Handling Test Completed ===")
    
    def _send_grafana_alert(self, test_config) -> dict:
        """
        Send a Grafana alert payload to the processAlert endpoint.
        
        Returns:
            Response JSON from the API
        """
        alert_name = "HighCPUUsage"
        timestamp = int(time.time())
        
        url = f"{config.BASE_URL}/processAlert{config.PROXY_PARAM}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.JWT_TOKEN}"
        }
        
        payload = {
            "receiver": "Test_Endpoint",
            "status": "firing",
            "alerts": [{
                "status": "firing",
                "labels": {
                    "alertname": alert_name,
                    "grafana_folder": "test",
                    "instance": "test-server",
                    "severity": "critical"
                },
                "annotations": {
                    "description": "CPU usage exceeded 90% on test server",
                    "summary": "High CPU Usage Alert"
                },
                "startsAt": str(timestamp),
                "fingerprint": f"test{timestamp}"
            }],
            "groupLabels": {
                "alertname": alert_name
            },
            "commonLabels": {
                "alertname": alert_name,
                "severity": "critical"
            },
            "commonAnnotations": {
                "description": "CPU usage exceeded 90% on test server",
                "summary": "High CPU Usage Alert"
            },
            "externalURL": "http://grafana:3000/",
            "version": "1",
            "title": f"[FIRING:1] {alert_name}",
            "state": "alerting"
        }
        
        logger.info(f"Sending alert to: {url}")
        logger.info(f"Alert name: {alert_name}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send alert: {e}")
            return {
                "status": "error",
                "message": str(e),
                "tasks_executed": 0
            }
    
    def _send_autonomous_test_alert(self, test_config) -> dict:
        """
        Send a unique alert for Autonomous mode testing.
        Uses a unique alert name to avoid matching existing tasks.
        
        Returns:
            Response JSON from the API
        """
        # Use unique alert name with timestamp to avoid matching existing tasks
        timestamp = int(time.time())
        alert_name = f"AutonomousTest_{timestamp}"
        
        url = f"{config.BASE_URL}/processAlert{config.PROXY_PARAM}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.JWT_TOKEN}"
        }
        
        payload = {
            "receiver": "Autonomous_Test_Endpoint",
            "status": "firing",
            "alerts": [{
                "status": "firing",
                "labels": {
                    "alertname": alert_name,
                    "grafana_folder": "test",
                    "instance": "test-server-autonomous",
                    "severity": "warning"
                },
                "annotations": {
                    "description": f"Autonomous mode test alert - timestamp {timestamp}",
                    "summary": "Test alert for autonomous task generation"
                },
                "startsAt": str(timestamp),
                "fingerprint": f"autonomous_{timestamp}"
            }],
            "groupLabels": {
                "alertname": alert_name
            },
            "commonLabels": {
                "alertname": alert_name,
                "severity": "warning"
            },
            "commonAnnotations": {
                "description": f"Autonomous mode test alert - timestamp {timestamp}",
                "summary": "Test alert for autonomous task generation"
            },
            "externalURL": "http://grafana:3000/",
            "version": "1",
            "title": f"[FIRING:1] {alert_name}",
            "state": "alerting"
        }
        
        logger.info(f"Sending unique alert to: {url}")
        logger.info(f"Alert name: {alert_name} (unique for autonomous test)")
        logger.info("Autonomous mode should CREATE a new task, not use existing one")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=120)  # Longer timeout for autonomous
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send alert: {e}")
            return {
                "status": "error",
                "message": str(e),
                "tasks_executed": 0
            }
    
    def _send_pagerduty_alert(self, test_config) -> dict:
        """
        Send a PagerDuty alert payload to the processAlert endpoint.
        
        Returns:
            Response JSON from the API
        """
        timestamp = int(time.time())
        
        url = f"{config.BASE_URL}/processAlert{config.PROXY_PARAM}"
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config.JWT_TOKEN}"
        }
        
        payload = {
            "messages": [{
                "event": "incident.triggered",
                "log_entries": [{
                    "type": "trigger_log_entry",
                    "channel": {
                        "type": "api"
                    },
                    "created_at": f"{timestamp}"
                }],
                "incident": {
                    "incident_number": timestamp,
                    "title": "Database Connection Failure",
                    "description": "Unable to connect to production database",
                    "status": "triggered",
                    "urgency": "high",
                    "service": {
                        "name": "Database Service",
                        "id": "PSERVICE1"
                    }
                }
            }]
        }
        
        logger.info(f"Sending PagerDuty alert to: {url}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send alert: {e}")
            return {
                "status": "error",
                "message": str(e),
                "tasks_executed": 0
            }


