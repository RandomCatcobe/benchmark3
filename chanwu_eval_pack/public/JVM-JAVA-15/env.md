# Environment For JVM-JAVA-15

- Runtime: JDK 17 and Maven with dependency download enabled.
- Package versions: `joda-time:joda-time 2.12.6` and `2.12.7`.
- Version switching: edit the `joda.time.version` property in `client/pom.xml`.
- Adapter/API surface: library-api.
- Probe shape: compile `client/src/main/java/Probe.java` with the Maven dependency classpath, then run `java` and parse one JSON object from stdout.
- Command shape: `mvn -q dependency:build-classpath -Dmdep.outputFile=cp.txt`, `javac -encoding UTF-8 -cp <cp> src/main/java/Probe.java`, `java -cp src/main/java;<cp> Probe`.
