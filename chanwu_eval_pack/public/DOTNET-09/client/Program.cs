using System.Globalization;
using CsvHelper;
using CsvHelper.Configuration;

using var reader = new StringReader("A;B\n");
using var csv = new CsvReader(reader, new CsvConfiguration(new CultureInfo("de-DE"))
{
    HasHeaderRecord = false
});
csv.Read();
var fields = csv.Context.Parser.Record ?? Array.Empty<string>();
Console.WriteLine(fields.Length);
Console.WriteLine(string.Join("|", fields));
