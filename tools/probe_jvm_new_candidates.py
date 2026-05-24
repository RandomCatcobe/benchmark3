from __future__ import annotations

import json
import shutil
import subprocess
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRATCH = ROOT / "data" / "verification" / "jvm_new_probe"


@dataclass(frozen=True)
class Candidate:
    slug: str
    group_id: str
    artifact_id: str
    old: str
    new: str
    class_name: str
    source: str
    source_url: str
    extra_dependencies: list[tuple[str, str, str]] = field(default_factory=list)


CANDIDATES = [
    Candidate(
        slug="jvm-jsoup-text-block-inline-spacing",
        group_id="org.jsoup",
        artifact_id="jsoup",
        old="1.15.3",
        new="1.15.4",
        class_name="Probe",
        source=r'''
import org.jsoup.Jsoup;

public class Probe {
    public static void main(String[] args) {
        String text = Jsoup.parse("<div>One</div><span>Two</span>").text();
        System.out.println("{\"text\":\"" + escape(text) + "\"}");
    }

    private static String escape(String text) {
        return text.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
''',
        source_url="https://github.com/jhy/jsoup/releases/tag/jsoup-1.15.4",
    ),
    Candidate(
        slug="jvm-commons-io-directory-contains-prefix",
        group_id="commons-io",
        artifact_id="commons-io",
        old="2.11.0",
        new="2.12.0",
        class_name="Probe",
        source=r'''
import org.apache.commons.io.FilenameUtils;

public class Probe {
    public static void main(String[] args) throws Exception {
        boolean contains = FilenameUtils.directoryContains("/tmp/base", "/tmp/base2/file.txt");
        System.out.println("{\"contains\":" + contains + "}");
    }
}
''',
        source_url="https://commons.apache.org/proper/commons-io/changes.html",
    ),
    Candidate(
        slug="jvm-commons-text-camelcase-only-delimiters",
        group_id="org.apache.commons",
        artifact_id="commons-text",
        old="1.9",
        new="1.10.0",
        class_name="Probe",
        source=r'''
import org.apache.commons.text.CaseUtils;

public class Probe {
    public static void main(String[] args) {
        String camel = CaseUtils.toCamelCase("---", false, '-', '_');
        System.out.println("{\"camel\":\"" + escape(camel) + "\"}");
    }

    private static String escape(String text) {
        return text.replace("\\", "\\\\").replace("\"", "\\\"");
    }
}
''',
        source_url="https://commons.apache.org/proper/commons-text/changes.html",
    ),
    Candidate(
        slug="jvm-commons-validator-iban-registry-update",
        group_id="commons-validator",
        artifact_id="commons-validator",
        old="1.8.0",
        new="1.9.0",
        class_name="Probe",
        source=r'''
import org.apache.commons.validator.routines.IBANValidator;

public class Probe {
    public static void main(String[] args) {
        IBANValidator validator = IBANValidator.getInstance();
        System.out.println("{\"SO\":" + validator.hasValidator("SO")
                + ",\"MN\":" + validator.hasValidator("MN")
                + ",\"OM\":" + validator.hasValidator("OM") + "}");
    }
}
''',
        source_url="https://commons.apache.org/proper/commons-validator/changes.html",
    ),
    Candidate(
        slug="jvm-joda-time-asia-almaty-2024-offset",
        group_id="joda-time",
        artifact_id="joda-time",
        old="2.12.6",
        new="2.12.7",
        class_name="Probe",
        source=r'''
import org.joda.time.DateTimeZone;
import org.joda.time.Instant;

public class Probe {
    public static void main(String[] args) {
        DateTimeZone zone = DateTimeZone.forID("Asia/Almaty");
        int offset = zone.getOffset(Instant.parse("2024-03-01T00:30:00Z"));
        System.out.println("{\"offset_seconds\":" + (offset / 1000) + "}");
    }
}
''',
        source_url="https://www.joda.org/joda-time/changes-report.html",
    ),
    Candidate(
        slug="jvm-libphonenumber-us-645-validity",
        group_id="com.googlecode.libphonenumber",
        artifact_id="libphonenumber",
        old="8.13.27",
        new="8.13.28",
        class_name="Probe",
        source=r'''
import com.google.i18n.phonenumbers.PhoneNumberUtil;
import com.google.i18n.phonenumbers.Phonenumber.PhoneNumber;

public class Probe {
    public static void main(String[] args) throws Exception {
        PhoneNumberUtil util = PhoneNumberUtil.getInstance();
        PhoneNumber number = util.parse("+16455551234", "US");
        boolean valid = util.isValidNumber(number);
        String type = util.getNumberType(number).toString();
        System.out.println("{\"valid\":" + valid + ",\"type\":\"" + type + "\"}");
    }
}
''',
        source_url="https://github.com/google/libphonenumber/releases/tag/v8.13.28",
    ),
    Candidate(
        slug="jvm-tika-warc-gz-detection",
        group_id="org.apache.tika",
        artifact_id="tika-core",
        old="2.8.0",
        new="2.9.0",
        class_name="Probe",
        source=r'''
import org.apache.tika.Tika;

public class Probe {
    public static void main(String[] args) {
        String type = new Tika().detect("sample.warc.gz");
        System.out.println("{\"warc_gz\":\"" + type + "\"}");
    }
}
''',
        source_url="https://tika.apache.org/2.9.0/",
        extra_dependencies=[("org.slf4j", "slf4j-nop", "2.0.7")],
    ),
]


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.mkdir(parents=True)
    kept: list[str] = []
    for candidate in CANDIDATES:
        result = probe(candidate)
        print(json.dumps(result, sort_keys=True), flush=True)
        if (
            result["old_exit"] == 0
            and result["new_exit"] == 0
            and result["old_stderr"] == ""
            and result["new_stderr"] == ""
            and result["old_stdout"] != result["new_stdout"]
        ):
            kept.append(candidate.slug)
    print(json.dumps({"kept": kept, "kept_count": len(kept)}, sort_keys=True), flush=True)
    return 0


def probe(candidate: Candidate) -> dict[str, object]:
    result = {
        "slug": candidate.slug,
        "module": f"{candidate.group_id}:{candidate.artifact_id}",
        "old": candidate.old,
        "new": candidate.new,
        "source": candidate.source_url,
    }
    for side, version in (("old", candidate.old), ("new", candidate.new)):
        work = SCRATCH / candidate.slug / side
        work.mkdir(parents=True, exist_ok=True)
        (work / f"{candidate.class_name}.java").write_text(candidate.source.strip() + "\n", encoding="utf-8")
        (work / "pom.xml").write_text(_pom(candidate, version), encoding="utf-8")
        cp_file = work / "cp.txt"
        dep = subprocess.run(
            [
                "mvn.cmd",
                "-q",
                "dependency:build-classpath",
                f"-Dmdep.outputFile={cp_file}",
            ],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=180,
        )
        if dep.returncode != 0:
            result[f"{side}_exit"] = dep.returncode
            result[f"{side}_stdout"] = dep.stdout.strip()
            result[f"{side}_stderr"] = dep.stderr.strip()
            continue
        cp = cp_file.read_text(encoding="utf-8").strip()
        sep = ";"
        compile_cp = cp
        javac = subprocess.run(
            ["javac", "-encoding", "UTF-8", "-cp", compile_cp, f"{candidate.class_name}.java"],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        if javac.returncode != 0:
            result[f"{side}_exit"] = javac.returncode
            result[f"{side}_stdout"] = javac.stdout.strip()
            result[f"{side}_stderr"] = javac.stderr.strip()
            continue
        runtime_cp = f".{sep}{cp}" if cp else "."
        run = subprocess.run(
            ["java", "-cp", runtime_cp, candidate.class_name],
            cwd=work,
            capture_output=True,
            text=True,
            check=False,
            timeout=60,
        )
        result[f"{side}_exit"] = run.returncode
        result[f"{side}_stdout"] = run.stdout.strip()
        result[f"{side}_stderr"] = run.stderr.strip()
    return result


def _pom(candidate: Candidate, version: str) -> str:
    return f'''<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 https://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>silentdrift</groupId>
  <artifactId>{candidate.slug}</artifactId>
  <version>1.0.0</version>
  <dependencies>
    <dependency>
      <groupId>{candidate.group_id}</groupId>
      <artifactId>{candidate.artifact_id}</artifactId>
      <version>{version}</version>
    </dependency>
{_extra_dependency_xml(candidate)}
  </dependencies>
</project>
'''


def _extra_dependency_xml(candidate: Candidate) -> str:
    lines: list[str] = []
    for group_id, artifact_id, version in candidate.extra_dependencies:
        lines.extend(
            [
                "    <dependency>",
                f"      <groupId>{group_id}</groupId>",
                f"      <artifactId>{artifact_id}</artifactId>",
                f"      <version>{version}</version>",
                "    </dependency>",
            ]
        )
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
