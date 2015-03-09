import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.SSLSession;

public class MyHostnameVerifier implements HostnameVerifier {
	public MyHostnameVerifier() {}
	public boolean verify(String string, SSLSession ssls) {
		return true;
	}
}