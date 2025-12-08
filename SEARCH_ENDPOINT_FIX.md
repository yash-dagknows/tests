# Search Endpoint Fix

## Issue Found
The search tests were failing with 404 errors because they were calling a non-existent endpoint.

**Wrong URL**: `/api/v1/tasks/search` ❌  
**Correct URL**: `/api/v1/tasks/` with `q=` parameter ✅

## Root Cause
The tests assumed a dedicated `/api/v1/tasks/search` endpoint existed, but the application actually implements search as part of the **task list endpoint** with a query parameter.

### How Search Actually Works (from UI logs):
```
GET /api/v1/tasks/?q=searchterm&page_key=0&page_size=10&knn.k=3&knn.nc=10&order_by=elastic
```

The search uses:
- Standard list endpoint: `/api/v1/tasks/`
- Query parameter: `q=searchterm`
- KNN (k-nearest neighbors) vector search
- Elasticsearch-based similarity matching

## Files Fixed

### 1. `tests/utils/api_client.py`

**TaskServiceClient.search_tasks()** (line 165):
```python
# Before:
return self.get(f"{self.api_base}/tasks/search", params=search_params)

# After:
search_params['q'] = query
return self.list_tasks(params=search_params)
```
Now uses the list endpoint with query parameter (matches UI behavior).

**ReqRouterClient.search_tasks()** (line 333):
```python
# Before:
return self.get('/api/tasks/search', params={'q': query})

# After:
return self.get('/api/tasks/', params={'q': query})
```

### 2. `tests/unit/taskservice/test_task_search.py`

Updated documentation to reflect that tests use the list endpoint with query parameter (same as UI).

## Verification

Now the search tests should work:

```bash
# Run search tests
docker-compose -f docker-compose-local.yml run --rm test-runner \
    pytest unit/taskservice/test_task_search.py::TestTaskSearch -v
```

Expected: All 4 search tests should pass.

## Test Coverage

The search tests now properly test:
- ✅ **test_search_tasks_by_title** - Search by task title using `q=` parameter
- ✅ **test_search_tasks_by_tag** - Search by tag using `q=` parameter  
- ✅ **test_search_tasks_by_description** - Search by description using `q=` parameter
- ✅ **test_search_nonexistent_task** - Search for non-existent tasks (should return empty)

## How Search Works in the Application

Based on UI behavior analysis:

1. **Endpoint**: `GET /api/v1/tasks/`
2. **Search Parameter**: `q=searchterm`
3. **Search Technology**: 
   - Elasticsearch KNN (k-nearest neighbors)
   - Vector similarity search
   - Searches across: title, description, tags, and script content
4. **Additional Parameters**:
   - `knn.k=3` - number of nearest neighbors
   - `knn.nc=10` - number of candidates
   - `order_by=elastic` - sort by Elasticsearch score
   - `page_size=10` - pagination

The tests now match this actual implementation behavior!

