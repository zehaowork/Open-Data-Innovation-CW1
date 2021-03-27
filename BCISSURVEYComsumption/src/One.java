import org.apache.jena.rdf.model.*;
import org.apache.jena.util.FileManager;
import org.apache.jena.query.* ;
import java.io.*;


public class One {

    static final String inputFileName = "BCISSurveyData.ttl";

    public static void main (String ... args) {

        // create an empty model
        Model model = ModelFactory.createDefaultModel();

        // use the FileManager to find the input file
        InputStream in = FileManager.get().open(inputFileName);
        if (in == null) {
            throw new IllegalArgumentException( "File: " + inputFileName + " not found");
        }

        // read the TTL file
        model.read( in, null, "TTL");


        String queryString = "SELECT ?s ?1 ?o  WHERE {?s ?p ?o .} LIMIT 100" ;
        Query query = QueryFactory.create(queryString) ;
        try (QueryExecution qexec = QueryExecutionFactory.create(query, model)) {
            ResultSet results = qexec.execSelect() ;
            for ( ; results.hasNext() ; )
            {
                QuerySolution soln = results.nextSolution() ;
                RDFNode s = soln.get("s");
                RDFNode p = soln.get("p");
                RDFNode o = soln.get("o");
                System.out.println(" { " + s + " " + p + " " + o + " . }");
            }

        }



	    /*
	    String queryString = "SELECT DISTINCT ?s ?p WHERE {\r\n" +
	    		"  ?s ?p <http://crime.psi.enakting.org/data/NorthWestRegion>\r\n" +
	    		"}" ;
	    Query query = QueryFactory.create(queryString) ;
	    try (QueryExecution qexec = QueryExecutionFactory.create(query, model)) {
	      ResultSet results = qexec.execSelect() ;
	      for ( ; results.hasNext() ; )
	      {
	        QuerySolution soln = results.nextSolution() ;
	        RDFNode s = soln.get("s");
			RDFNode p = soln.get("p");
			System.out.println(" { " + s + " " + p +  " . }");
	      }

	    }
	  */


        String tope = "tope";

    }

}
