# Environment For JVM-JAVA-17

- Runtime: JDK 17 and Maven with dependency download enabled.
- Package versions: `org.apache.tika:tika-core 2.8.0` and `2.9.0`.
- Support dependency: `org.slf4j:slf4j-nop 2.0.7` to suppress provider warning noise.
- Version switching: edit the `tika.version` property in `client/pom.xml`.
- Adapter/API surface: library-api.
- Probe shape: compile `client/src/main/java/Probe.java` with the Maven dependency classpath, then run `java` and parse one JSON object from stdout.
- Command shape: `mvn -q dependency:build-classpath -Dmdep.outputFile=cp.txt`, `javac -encoding UTF-8 -cp <cp> src/main/java/Probe.java`, `java -cp src/main/java;<cp> Probe`.
