import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.MalformedURLException;
import java.net.URL;
import java.security.Security;
import java.security.KeyStore;
import java.security.Provider;
import java.security.cert.X509Certificate;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.ManagerFactoryParameters;
import javax.net.ssl.TrustManager;
import javax.net.ssl.TrustManagerFactorySpi;
import javax.net.ssl.X509TrustManager;
import javax.net.ssl.SSLSession;

public class MySSLProvider extends Provider {
	public MySSLProvider() {
		super("MySSLProvider", 1.0, "Trust certificates");
		put("TrustManagerFactory.TrustAllCertificates",
				MyTrustManagerFactory.class.getName());
	}

	protected static class MyTrustManagerFactory extends TrustManagerFactorySpi {
		public MyTrustManagerFactory() {
		}

		protected void engineInit(KeyStore keystore) {
		}

		protected void engineInit(ManagerFactoryParameters mgrparams) {
		}

		protected TrustManager[] engineGetTrustManagers() {
			return new TrustManager[] { new MyX509TrustManager() };
		}
	}

	protected static class MyX509TrustManager implements X509TrustManager {
		public void checkClientTrusted(X509Certificate[] chain, String authType) {
		}

		public void checkServerTrusted(X509Certificate[] chain, String authType) {
		}

		public X509Certificate[] getAcceptedIssuers() {
			return null;
		}
	}

	
	
	public static void main(String[] args) {
		java.security.Security.addProvider(new MySSLProvider());
		java.security.Security.setProperty("ssl.TrustManagerFactory.algorithm",
				"TrustAllCertificates");

		HttpsURLConnection.setDefaultHostnameVerifier(new MyHostnameVerifier());

		try {
			URL url = new URL(
					"https://od-c3-nsve:8443/NetworkServicesManagerAPI/v1/top/catalog");
			HttpsURLConnection con = (HttpsURLConnection) url.openConnection();
			
			
			con.setRequestProperty("Accept", "application/xml");
			con.setRequestProperty("Content-Type", "application/xml");
			con.setRequestProperty("Authorization", "Basic YWRtaW46YWRtaW4=");
			con.setDoInput(true);
			//con.setDoOutput(true);
			//con.setDefaultAllowUserInteraction(false); 
			//con.setRequestMethod("GET");
	
			
			//DataOutputStream output = new DataOutputStream(con.getOutputStream());
			//System.out.println("Resp Code: "+con.getResponseCode()); 
			//System.out.println("Resp Message: "+ con.getResponseMessage()); 
			
			// get ready to read the response from the cgi script
			DataInputStream input = new DataInputStream(con.getInputStream());

			//read in each character until end-of-stream is detected
			for (int c = input.read(); c != -1; c = input.read())
				System.out.print((char) c);
			input.close();

		} catch (Exception e) {
			System.out.print(e);
		}

		System.out.println("\ndone");
	}
}

