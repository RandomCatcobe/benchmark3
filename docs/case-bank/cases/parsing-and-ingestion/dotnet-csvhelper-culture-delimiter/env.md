# Environment For DOTNET-09

        - Old version: CsvHelper 9.2.3.
        - New version: CsvHelper 10.0.0.
        - Adapter/API surface: library-api, csv-parser.
        - Runtime: .NET SDK with CsvHelper installed.
- Version switching: restore with CsvHelper 9.2.3 for old and 10.0.0 for new.
- Probe shape: run Program.cs and compare field count plus joined fields.
