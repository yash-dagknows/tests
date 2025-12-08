# Global Search (gsearch) vs UI Search Comparison

## Summary

There are **TWO different search endpoints** in your application:

| Feature | **UI Search** (List Endpoint) | **Global Search** (gsearch) |
|---------|-------------------------------|---------------------------|
| **Endpoint** | `GET /api/v1/tasks/` | `GET /api/v1/tasks/gsearch` |
| **Purpose** | Single workspace/site search | Multi-site/cross-workspace search |
| **Scope** | Current workspace only | Your instance + Community |
| **Used By** | Main UI search bar | Special federated search feature |
| **KNN Search** | ✅ Yes (Elasticsearch vector search) | ✅ Yes |
| **Pagination** | Simple (page_key, page_size) | Complex (base64 encoded multi-source) |
| **Filtering** | Rich (tags, user, workspace, etc.) | Basic (q, order_by only) |

---

## 1. UI Search (What You Use Daily)

### Endpoint
```
GET /api/v1/tasks/?q=searchterm&page_key=0&page_size=10&knn.k=3&knn.nc=10&order_by=elastic
```

### Implementation
**File**: `taskservice/src/app.py` - `TaskResource.doListTasks()` (line 723)

### Features

#### Rich Query Parameters:
- **`q`** - Search query (text/semantic search)
- **`tags`** - Filter by tags (comma-separated)
- **`userid`** - Filter by creator
- **`collaborator`** - Filter by collaborator
- **`workspace_id`** - Filter by workspace
- **`favorited`** - Show only favorited tasks
- **`not_parent_count`** - Filter tasks without parents
- **`with_pending_perms`** - Include pending permissions
- **`order_by`** - Sort order (elastic, title, created_at, etc.)
- **`knn.k`** - K-nearest neighbors count (vector search)
- **`knn.nc`** - Number of candidates for KNN
- **`knn.similarity`** - Minimum similarity score
- **`alert_source`** - Filter by alert source
- **`alert_name`** - Filter by alert name
- **`is_tooltask_search`** - Search only tool tasks

#### Workspace Scoped:
```python
req = tasks_pb2.ListTasksRequest(
    query=q,
    workspace_id=request.args.get("workspace_id", ""),
    wsid=self.argOrParam("wsid"),  # Current workspace
    ...
)
```
**Searches within your current workspace only** (unless workspace_id specified).

#### KNN Vector Search:
```python
if request.args.get("knn.k", ""):
    req.experimental["knn.k"] = int(request.args.get("knn.k", "-1"))
    req.experimental["knn.nc"] = int(request.args.get("knn.nc", "-1"))
    req.experimental["knn.similarity"] = float(request.args.get("knn.similarity", "-1"))
```
Uses **Elasticsearch vector similarity search** - finds semantically similar tasks.

#### Response Format:
```json
{
  "tasks": [...],
  "pagination": {
    "page_key": "...",
    "has_more": true/false
  }
}
```

---

## 2. Global Search (gsearch)

### Endpoint
```
GET /api/v1/tasks/gsearch?q=searchterm&page_key=<base64>&order_by=elastic
```

### Implementation
**File**: `taskservice/src/app.py` - `TaskSearchResource.get()` (line 2524)

### Features

#### Multi-Site Federated Search:
```python
searchiters = []
for index, pagekey in enumerate(page_keys):
    if index == 0:
        search_url = self.url("/api/v1/tasks")  # Your instance
    else:
        search_url = self.url("/api/tasks", community_url)  # Community
    searchiter = SearchIterator(search_url, *pagekey, **search_params)
    searchiters.append(searchiter)
```

**Searches MULTIPLE sources**:
1. **Your local instance** - Your workspace/organization
2. **Community URL** - External DagKnows community (if configured)

#### Limited Parameters:
- **`q`** - Search query only
- **`order_by`** - Sort order
- **`page_key`** - Base64 encoded pagination for multiple sources

No filtering by tags, user, workspace, etc.

#### Complex Pagination:
```python
# page_key is base64 encoded: "local_page:size,community_page:size"
page_keys = [x.strip() for x in b64decode(page_key).decode("utf-8").split(",")]
# Example: ["0:10", "0:10"] for first page of both sources
```

Each source (local + community) has its own pagination state.

#### Response Format:
```json
{
  "results": [
    // Merged and sorted results from multiple sources
  ]
}
```

#### Configuration:
```python
community_url = os.environ.get("COMMUNITY_URL", "").strip()
enable_community = community_url != ""
```
Requires **`COMMUNITY_URL`** environment variable to search external sources.

---

## When to Use Each

### Use **UI Search** (List Endpoint) When:
- ✅ Searching within your workspace
- ✅ Need to filter by tags, user, workspace
- ✅ Want KNN vector similarity search
- ✅ Need pagination through large result sets
- ✅ Building normal user-facing features

**This is what 99% of users interact with daily.**

### Use **Global Search** (gsearch) When:
- ✅ Searching across your instance AND external community
- ✅ Finding tasks shared by other organizations
- ✅ Federated/multi-tenant search scenarios
- ✅ Building a "search marketplace" feature

**This is for advanced federated search scenarios.**

---

## From Your Logs

Your UI search shows:
```
GET /api/v1/tasks/?q=wrfgrfg&page_key=0&page_size=10&knn.k=3&knn.nc=10&order_by=elastic

taskservice-1  | Searching by query:  wrfgrfg
taskservice-1  | KNN SEARCH RESULTS
taskservice-1  | KNN Parameters: k=3.0, num_candidates=10.0
```

This is:
- ✅ **UI Search** (list endpoint)
- ✅ Using KNN vector search
- ✅ Workspace-scoped
- ✅ Rich filtering capabilities

---

## Test Recommendations

### ✅ Your Tests Should Use UI Search

The tests now correctly use `/api/v1/tasks/?q=...` because:
1. **This is what users actually use** (matches UI behavior)
2. **More powerful** (filters, KNN, etc.)
3. **Workspace-scoped** (proper tenant isolation)
4. **Better test coverage** of real functionality

### ⚠️ Global Search Tests (Optional)

If you want to test `gsearch`, create **separate tests** in a file like:
- `tests/unit/taskservice/test_global_search.py`

But only if:
- You use `COMMUNITY_URL` in production
- You have federated search features
- Users actually use this endpoint

---

## Architecture Insight

```
┌─────────────────────────────────────────────────┐
│  UI Search Bar                                  │
│  "Search tasks..."                              │
└──────────────┬──────────────────────────────────┘
               │
               ▼
       GET /api/v1/tasks/?q=...
               │
               ▼
       ┌───────────────────┐
       │  TaskResource     │──► Elasticsearch KNN
       │  doListTasks()    │
       └───────────────────┘
               │
               ▼
       Current Workspace Results
```

```
┌─────────────────────────────────────────────────┐
│  Special "Search Community" Feature (if exists) │
└──────────────┬──────────────────────────────────┘
               │
               ▼
       GET /api/v1/tasks/gsearch
               │
               ▼
       ┌────────────────────────┐
       │  TaskSearchResource    │
       │  get()                 │
       └───────┬────────────────┘
               │
         ┌─────┴─────┐
         ▼           ▼
    Local Tasks  + Community Tasks
         │           │
         └─────┬─────┘
               ▼
       Merged Results
```

---

## Bottom Line

**For your tests**: ✅ Use `/api/v1/tasks/?q=...` (UI Search)  
**For federated search**: ℹ️ Use `/api/v1/tasks/gsearch` (Global Search)

Your current test fix is **correct** - it matches what real users do!

