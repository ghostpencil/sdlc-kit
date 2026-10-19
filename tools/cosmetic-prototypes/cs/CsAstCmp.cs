// usage: dotnet CsAstCmp.dll before after -> exit 0 equal, 1 different, 2 parse error
using System;
using System.IO;
using System.Linq;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;
static class CsAstCmp {
  static int Main(string[] a) {
    var t1 = CSharpSyntaxTree.ParseText(File.ReadAllText(a[0]));
    var t2 = CSharpSyntaxTree.ParseText(File.ReadAllText(a[1]));
    if (t1.GetDiagnostics().Concat(t2.GetDiagnostics()).Any(d => d.Severity == DiagnosticSeverity.Error)) return 2;
    // IsEquivalentTo compares structure + token text, ignoring trivia (whitespace, comments, directives)
    return t1.IsEquivalentTo(t2, topLevel: false) ? 0 : 1;
  }
}
