
import java.io.StringReader;
import java.io.FileReader;

import javax.xml.XMLConstants;
import javax.xml.transform.stream.StreamSource;
import javax.xml.validation.Schema;
import javax.xml.validation.SchemaFactory;
import javax.xml.validation.Validator;

import org.xml.sax.ErrorHandler;
import org.xml.sax.SAXException;
import org.xml.sax.SAXParseException;

import java.io.*;

public class ValidateXML {
	
	public boolean validateXML() {

		System.out.println("Richiesta " + this.getClass());

		MyErrorHandler errorHandler = new MyErrorHandler();
		try {

			String xmlFilePath = "/Users/huhe/Install/workspace/NSM-NBAPI-Jython/response/create/response-create-default/My-Default-Internet-Dynamic-PAT-Service-create-001.xml";
			String xml = readFile(xmlFilePath);
			System.out.println(xml);
			
			StreamSource xsdStreamSource1 = new StreamSource(new FileReader("/Users/huhe/Install/workspace/NSM-NBAPI-Jython/schema/nsm.xsd"));
			StreamSource xsdStreamSource2 = new StreamSource(new FileReader("/Users/huhe/Install/workspace/NSM-NBAPI-Jython/schema/ATOM-1.0.xsd"));
			StreamSource xsdStreamSource3 = new StreamSource(new FileReader("/Users/huhe/Install/workspace/NSM-NBAPI-Jython/schema/XML-Namespace-1998.xsd"));
			
			StreamSource[] xsdStreamSources = new StreamSource[3];
			xsdStreamSources[0] = xsdStreamSource1;
			xsdStreamSources[1] = xsdStreamSource2;
			xsdStreamSources[2] = xsdStreamSource3;

			SchemaFactory factory = SchemaFactory.newInstance(XMLConstants.W3C_XML_SCHEMA_NS_URI);
			Schema schema = factory.newSchema(xsdStreamSources);

			Validator validator = schema.newValidator();
			validator.setErrorHandler(errorHandler);
			validator.validate(new StreamSource(new StringReader(xml)));

		} catch (Exception e) {
			e.printStackTrace();
			return false;
		}

		System.out.println("PASSED");
		
		String getResult = errorHandler.getResult();
		if (getResult.isEmpty()) {
			System.out.println("The XML is Well Formed and VALID");
			return true;
		}
		else {
			System.out.println(getResult);
			return false;
		}
	}

	public static void main(String[] args) {
		ValidateXML validate = new ValidateXML();
		validate.validateXML();
	}
	
	private String readFile( String file ) throws IOException {
	    BufferedReader reader = new BufferedReader( new FileReader (file));
	    String         line = null;
	    StringBuilder  stringBuilder = new StringBuilder();
	    String         ls = System.getProperty("line.separator");

	    while( ( line = reader.readLine() ) != null ) {
	        stringBuilder.append( line );
	        stringBuilder.append( ls );
	    }

	    return stringBuilder.toString();
	}
	
	static class MyErrorHandler implements ErrorHandler {

		StringBuilder result = new StringBuilder();

		public void fatalError(SAXParseException e) throws SAXException {
			result.append(e.toString());
		}

		public void error(SAXParseException e) throws SAXException {
			result.append(e.toString());
		}

		public void warning(SAXParseException e) throws SAXException {
			result.append(e.toString());
		}

		public String getResult() {
			return result.toString();
		}
	}
}
