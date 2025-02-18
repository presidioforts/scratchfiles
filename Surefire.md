
<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.0.0-M5</version>
  <configuration>
    <!-- Adjust the fork count as desired (e.g., "1", "2", or "1C" for one fork per core). -->
    <forkCount>1C</forkCount>
    <!-- Increase the memory heap to avoid OutOfMemoryError. Adjust -Xmx as needed. -->
    <argLine>-Xmx1024m</argLine>
  </configuration>
</plugin>
