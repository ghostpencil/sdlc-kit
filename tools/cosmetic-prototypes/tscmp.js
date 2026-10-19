// usage: node tscmp.js before after  -> exit 0 equal, 1 different, 2 parse error
const ts = require(require.resolve('typescript', {paths: [process.cwd(), __dirname]}));
const fs = require('fs');
function sig(file) {
  const src = fs.readFileSync(file, 'utf8');
  const kind = /\.[cm]?tsx?$/.test(file) ? (file.endsWith('x') ? ts.ScriptKind.TSX : ts.ScriptKind.TS)
             : (file.endsWith('x') ? ts.ScriptKind.JSX : ts.ScriptKind.JS);
  const sf = ts.createSourceFile(file, src, ts.ScriptTarget.Latest, false, kind);
  if (sf.parseDiagnostics && sf.parseDiagnostics.length) return null;
  const out = [];
  (function walk(n) {
    out.push(n.kind);
    // leaf tokens carry text (identifiers, literals, keywords-as-names)
    if (n.text !== undefined && ts.isTokenKind ? ts.isTokenKind(n.kind) || ts.isLiteralKind(n.kind) || n.kind === ts.SyntaxKind.Identifier : true) out.push(JSON.stringify(n.text));
    out.push('(');
    ts.forEachChild(n, walk);   // forEachChild does not visit JSDoc or trivia
    out.push(')');
  })(sf);
  return out.join(' ');
}
const a = sig(process.argv[2]), b = sig(process.argv[3]);
if (a === null || b === null) process.exit(2);
process.exit(a === b ? 0 : 1);
