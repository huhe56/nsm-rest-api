import java.io.File;
import java.util.concurrent.TimeUnit;
import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.Select;
import org.apache.commons.io.FileUtils;

public class ACP {
	private WebDriver driver;
	private String baseUrl;
	
	public void start() throws Exception {
		driver = new FirefoxDriver();
		baseUrl = "https://od-c3-nsve:8443";
		driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
		driver.get(baseUrl + "/acp/");
		driver.findElement(By.cssSelector("input[type=\"button\"]")).click();
		new Select(driver.findElement(By.cssSelector("select"))).selectByVisibleText("Clear persisted policy files");
		driver.switchTo().alert().accept();
		new Select(driver.findElement(By.cssSelector("select"))).selectByVisibleText("Start");
		Thread.sleep(5000);
		File scrFile = ((TakesScreenshot)driver).getScreenshotAs(OutputType.FILE);
		FileUtils.copyFile(scrFile, new File("c:\\tmp\\screenshot.png"));
		driver.close();
	}
	
	public static void main(String[] args) {
		ACP acp = new ACP();
		try {
			acp.start();
		}
		catch(Exception e) {
			e.printStackTrace();
		}
	}
}
