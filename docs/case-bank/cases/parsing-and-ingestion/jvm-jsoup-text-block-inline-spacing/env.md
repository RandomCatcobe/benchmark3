# Environment For JVM-JAVA-11

- Runtime: JDK 17 and Maven with dependency download enabled.
- Package versions: `org.jsoup:jsoup 1.15.3` and `1.15.4`.
- Version switching: edit the `jsoup.version` property in `client/pom.xml`.
- Adapter/API surface: library-api.
- Probe shape: compile `client/src/main/java/Probe.java` with the Maven dependency classpath, then run `java` and parse one JSON object from stdout.
- Command shape: `mvn -q dependency:build-classpath -Dmdep.outputFile=cp.txt`, `javac -encoding UTF-8 -cp <cp> src/main/java/Probe.java`, `java -cp src/main/java;<cp> Probe`.
