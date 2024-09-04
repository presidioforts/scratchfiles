To define and configure critical metrics for MongoDB, you should focus on the following key areas: **CPU usage, memory, connection pool size, query performance, and disk space**. Here's how to configure and monitor these values, particularly focusing on **query performance**.

### 1. **CPU Usage**:
   - **Critical Metric**: CPU utilization should be monitored continuously. If CPU usage goes above 80-90%, MongoDB may be under heavy load.
   - **Monitoring**: Use MongoDB metrics from tools like **Prometheus**, **Datadog**, or **Cloudwatch** (if using cloud services).
   - **Alert Threshold**: Set alerts when CPU usage exceeds 85%.
   - **Command**: 
     ```bash
     db.serverStatus().metrics.cpu
     ```
   - **Monitoring Tools**: Use tools like **mongostat** or **top** to watch real-time CPU usage.

### 2. **Memory Usage**:
   - **Critical Metric**: MongoDB keeps data in memory for faster access. Ensure that memory usage doesn’t reach system limits. High memory usage can cause swapping, leading to performance issues.
   - **Monitoring**: Memory stats can be monitored via `db.serverStatus()` or **Prometheus**.
   - **Alert Threshold**: Set an alert when memory usage reaches 85% of the available memory.
   - **Command**:
     ```bash
     db.serverStatus().wiredTiger.cache['bytes currently in the cache']
     ```

### 3. **Connection Pool Size**:
   - **Critical Metric**: MongoDB’s connection pool should be monitored to ensure that connections don’t max out. Too many connections can overwhelm the database.
   - **Monitoring**: Monitor the current number of connections with:
     ```bash
     db.serverStatus().connections
     ```
   - **Alert Threshold**: Set an alert when active connections reach 80% of the connection pool limit. For example, if your MongoDB is configured for 1000 max connections, set the alert when 800 are in use.
   - **Monitoring Tools**: Tools like **mongostat**, **Prometheus**, and **Grafana** can help visualize connection metrics.

### 4. **Query Performance (Specific Configuration)**:
   **Critical Metric**: Slow query performance is a key indicator of database performance issues. MongoDB provides tools like **Profiler** and **Slow Query Logging** to monitor and optimize queries.

   #### Steps to Configure Slow Query Logging:
   - **Enable Slow Query Log**:
     ```bash
     db.setProfilingLevel(1, { slowms: 100 })
     ```
     This will log queries taking longer than 100 milliseconds. You can adjust the threshold (e.g., to 200ms or 500ms) depending on your performance goals.
   - **Profiling Levels**:
     - **Level 0**: Profiling is off (default).
     - **Level 1**: Logs slow queries (defined by `slowms`).
     - **Level 2**: Logs **all** queries.

   - **Examine Slow Queries**:
     To view slow queries from the profiler:
     ```bash
     db.system.profile.find({ millis: { $gt: 100 } })
     ```
     This will show all queries taking longer than 100ms.

   #### Optimizing Query Performance:
   - **Indexing**: Make sure your frequently queried fields are indexed.
   - **Query Patterns**: Use projections (`.find({}, { field1: 1 })`) to limit the fields returned in the results.
   - **Aggregation**: If you're using aggregation pipelines, monitor the complexity of the pipeline to avoid excessive CPU or memory usage.
   - **Cache Usage**: Monitor query cache hit rates to ensure queries are optimized to use the cache effectively.

   #### Alert Threshold for Query Performance:
   - **Threshold**: Set a threshold for slow query alerts, e.g., when more than 5% of queries exceed 200ms.
   - **Monitoring Tools**: Tools like **Grafana** or **Datadog** can be configured to visualize and alert when slow queries exceed the defined threshold.

### 5. **Disk Space**:
   - **Critical Metric**: MongoDB requires enough disk space for data, logs, and journaling. Disk space exhaustion can crash the database.
   - **Monitoring**: Monitor disk space usage on the partition where MongoDB is storing data. Use tools like **Prometheus**, **Nagios**, or **df -h** for real-time disk space usage.
   - **Alert Threshold**: Set an alert if disk usage reaches 85% capacity.
   - **Command**:
     ```bash
     db.serverStatus().wiredTiger.cache['maximum bytes configured']
     ```

### Tools to Use for Monitoring:

- **Prometheus** (with **MongoDB Exporter**): Collects MongoDB metrics and integrates with **Grafana** for visual dashboards.
- **Mongostat**: A built-in MongoDB tool to provide real-time statistics on MongoDB performance, including CPU, connections, and disk usage.
- **MongoDB Atlas** (if using a managed service): Provides built-in dashboards and alerting for most of these metrics.

### Summary of Alerts Configuration:
1. **CPU Usage**: Set an alert at 85% CPU usage.
2. **Memory Usage**: Set an alert at 85% memory consumption.
3. **Connection Pool Size**: Set an alert when 80% of connections are used.
4. **Query Performance**: Monitor slow queries, set alerts when more than 5% exceed the `slowms` threshold.
5. **Disk Space**: Set an alert at 85% disk usage.

By monitoring and configuring these values, you can stay proactive and catch MongoDB performance issues before they impact production.
