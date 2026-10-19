// usage: java JavaAstCmp.java before after -> exit 0 equal, 1 different, 2 parse error
import com.sun.source.tree.*;
import com.sun.source.util.*;
import javax.tools.*;
import java.net.URI;
import java.nio.file.*;
import java.util.*;

public class JavaAstCmp {
  static String sig(Path p) throws Exception {
    String src = Files.readString(p);
    JavaCompiler jc = ToolProvider.getSystemJavaCompiler();
    DiagnosticCollector<JavaFileObject> diags = new DiagnosticCollector<>();
    JavaFileObject fo = new SimpleJavaFileObject(URI.create("string:///" + p.getFileName()), JavaFileObject.Kind.SOURCE) {
      @Override public CharSequence getCharContent(boolean b) { return src; }
    };
    JavacTask task = (JavacTask) jc.getTask(null, null, diags, List.of("-proc:none"), null, List.of(fo));
    Iterable<? extends CompilationUnitTree> units = task.parse();   // parse only: no symbol resolution, no classpath
    for (Diagnostic<?> d : diags.getDiagnostics()) if (d.getKind() == Diagnostic.Kind.ERROR) return null;
    StringBuilder sb = new StringBuilder();
    for (CompilationUnitTree u : units) {
      new TreeScanner<Void, Void>() {
        @Override public Void scan(Tree t, Void v) {
          if (t == null) return null;
          sb.append(t.getKind()).append('(');
          if (t instanceof IdentifierTree i) sb.append(i.getName());
          else if (t instanceof MemberSelectTree m) sb.append(m.getIdentifier());
          else if (t instanceof LiteralTree l) sb.append(String.valueOf(l.getValue()));
          else if (t instanceof MethodTree m) sb.append(m.getName());
          else if (t instanceof ClassTree c) sb.append(c.getSimpleName());
          else if (t instanceof VariableTree vt) sb.append(vt.getName());
          else if (t instanceof ModifiersTree mt) sb.append(mt.getFlags());
          else if (t instanceof PrimitiveTypeTree pt) sb.append(pt.getPrimitiveTypeKind());
          super.scan(t, v);
          sb.append(')');
          return null;
        }
      }.scan(u, null);
    }
    return sb.toString();
  }
  public static void main(String[] a) throws Exception {
    String x = sig(Path.of(a[0])), y = sig(Path.of(a[1]));
    if (x == null || y == null) System.exit(2);
    System.exit(x.equals(y) ? 0 : 1);
  }
}
