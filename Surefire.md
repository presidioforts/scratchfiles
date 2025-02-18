
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


<plugin>
  <groupId>org.apache.maven.plugins</groupId>
  <artifactId>maven-surefire-plugin</artifactId>
  <version>3.1.0</version>
  <configuration>
    <!-- Use a single fork or one per CPU core (1C). -->
    <forkCount>1</forkCount>
    <!-- Usually best to reuse forks for performance, unless you have memory leaks. -->
    <reuseForks>true</reuseForks>
    <!-- Fail the build on any test failures. -->
    <testFailureIgnore>false</testFailureIgnore>
    <!-- Keep or remove the skip property as needed. -->
    <skipTests>${skip.unit.tests}</skipTests>

    <!-- Optionally increase heap memory if you have out-of-memory issues: -->
    <argLine>-Xmx1024m</argLine>
  </configuration>
</plugin>
