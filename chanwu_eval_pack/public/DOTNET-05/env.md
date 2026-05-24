# Environment For DOTNET-05

        - Old version: Microsoft.Extensions.Configuration.Binder 6.x.
        - New version: Microsoft.Extensions.Configuration.Binder 7.x.
        - Adapter/API surface: configuration-binder, library-api.
        - Runtime: .NET SDK with Microsoft.Extensions.Configuration.Binder installed.
- Version switching: restore with Binder 6.x for old and 7.x for new.
- Probe shape: run Program.cs and compare the pipe-delimited value list from stdout.
