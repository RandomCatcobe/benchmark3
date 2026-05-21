using Microsoft.Extensions.Configuration;

var seed = new Dictionary<string, string?>
{
    ["Key:0"] = "NewValue"
};
var config = new ConfigurationBuilder().AddInMemoryCollection(seed).Build();
var target = new Dictionary<string, string[]>
{
    ["Key"] = new[] { "InitialValue" }
};

config.Bind(target);
Console.WriteLine(string.Join("|", target["Key"]));
