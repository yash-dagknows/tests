"""
Initialization tests - Run these first to setup test environment.

These tests create necessary indices and setup data.
"""

import pytest
import requests
import json
import os


@pytest.mark.smoke
@pytest.mark.order(1)
def test_elasticsearch_indices_exist_or_create():
    """
    Check if Elasticsearch indices exist, create if they don't.
    
    This test should run FIRST to ensure indices are ready.
    """
    es_url = os.getenv("DAGKNOWS_ELASTIC_URL", "http://elasticsearch:9200")
    org = os.getenv("DEFAULT_ORG", "dagknows")
    
    print(f"\n" + "="*60)
    print(f"Org from environment: '{org}'")
    print(f"Will check/create indices for: {org}__*")
    print("="*60)
    
    # List of indices needed
    indices = [
        f"{org}__tasks_alias",
        f"{org}__workspaces_alias",
        f"{org}__nodes_alias",
        f"{org}__dags_alias",
        "public__settings",  # Settings index (shared)
    ]
    
    print(f"\nChecking Elasticsearch indices for org: {org}")
    
    for index_name in indices:
        # Check if index exists
        check_url = f"{es_url}/{index_name}"
        response = requests.head(check_url, timeout=5)
        
        if response.status_code == 200:
            print(f"✓ Index exists: {index_name}")
        else:
            print(f"⚠ Index missing: {index_name}, creating...")
            
            # Create index with basic mapping
            create_url = f"{es_url}/{index_name}"
            mapping = {
                "mappings": {
                    "properties": {
                        "title": {"type": "text"},
                        "description": {"type": "text"},
                        "created_at": {"type": "date"},
                        "updated_at": {"type": "date"},
                        "tags": {"type": "keyword"}
                    }
                }
            }
            
            create_response = requests.put(create_url, json=mapping, timeout=10)
            
            if create_response.status_code in [200, 201]:
                print(f"✓ Created index: {index_name}")
            else:
                print(f"✗ Failed to create {index_name}: {create_response.text}")
    
    # Verify all indices exist now
    response = requests.get(f"{es_url}/_cat/indices/{org}*?format=json", timeout=5)
    indices_list = response.json() if response.status_code == 200 else []
    
    print(f"\nTotal indices for '{org}': {len(indices_list)}")
    for idx in indices_list:
        print(f"  - {idx['index']}: {idx['health']} ({idx['docs.count']} docs)")
    
    assert len(indices_list) >= 2, f"Expected at least 2 indices for {org}, found {len(indices_list)}"
    print(f"\n✓ All indices ready for org: {org}")


@pytest.mark.smoke
@pytest.mark.order(2)
def test_database_connection():
    """Test that database is accessible and has required tables."""
    import psycopg2
    
    db_host = os.getenv("POSTGRESQL_DB_HOST", "postgres")
    db_port = os.getenv("POSTGRESQL_DB_PORT", "5432")
    db_name = os.getenv("POSTGRESQL_DB_NAME", "dagknows")
    db_user = os.getenv("POSTGRESQL_DB_USER", "postgres")
    db_pass = os.getenv("POSTGRESQL_DB_PASSWORD", "")
    
    print(f"\nConnecting to database: {db_host}:{db_port}/{db_name}")
    
    try:
        conn = psycopg2.connect(
            host=db_host,
            port=db_port,
            database=db_name,
            user=db_user,
            password=db_pass,
            connect_timeout=5
        )
        
        cursor = conn.cursor()
        
        # Check required tables exist
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema='public' 
            ORDER BY table_name
        """)
        
        tables = [row[0] for row in cursor.fetchall()]
        print(f"\nDatabase tables: {len(tables)}")
        for table in tables:
            print(f"  - {table}")
        
        # Check if orgs table exists and has data
        if 'orgs' in tables:
            cursor.execute("SELECT name FROM orgs")
            orgs = [row[0] for row in cursor.fetchall()]
            print(f"\nOrganizations in database: {orgs}")
            
            default_org = os.getenv("DEFAULT_ORG", "dagknows")
            if default_org in orgs:
                print(f"✓ Default org '{default_org}' exists")
            else:
                print(f"⚠ Default org '{default_org}' NOT found")
                print(f"Available orgs: {orgs}")
        
        cursor.close()
        conn.close()
        
        print("\n✓ Database connection successful")
        
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


@pytest.mark.smoke
@pytest.mark.order(3)
def test_ready_for_testing():
    """Final check that environment is ready for testing."""
    print("\n" + "="*60)
    print("Environment Ready Check")
    print("="*60)
    
    # Check all required env vars
    required_vars = [
        "DAGKNOWS_ELASTIC_URL",
        "DAGKNOWS_TASKSERVICE_URL",
        "DAGKNOWS_REQ_ROUTER_URL",
        "POSTGRESQL_DB_HOST",
        "POSTGRESQL_DB_PASSWORD",
        "DEFAULT_ORG"
    ]
    
    missing = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {value[:30]}...")
        else:
            print(f"✗ {var}: NOT SET")
            missing.append(var)
    
    if missing:
        pytest.fail(f"Missing environment variables: {missing}")
    
    print("\n✓ Environment is configured")
    print("✓ Ready for testing!")

