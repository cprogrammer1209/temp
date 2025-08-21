package StepDefinition;

import java.time.Duration;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

//import dev.failsafe.internal.util.Assert;
import io.cucumber.java.en.And;
import io.cucumber.java.en.Given;
import io.cucumber.java.en.Then;
import io.cucumber.java.en.When;

public class paytmtravel {
	WebDriver driver;
	WebDriverWait wait;
	JavascriptExecutor jse;

	public paytmtravel() {

		this.driver = ScreenshotHook.getDriver();
		this.wait = new WebDriverWait(driver, Duration.ofSeconds(10));
		this.jse = (JavascriptExecutor) driver;
	}

	@Given("login to paytm travel")
	public void login_to_paytm_travel() throws Exception {

		try {
			// Open the login page
			driver.get("https://tickets.paytm.com/");

			Thread.sleep(10000);

		} catch (Exception e) {
			e.printStackTrace();
			throw e;
		}
	}

	@When("click bus")
	public void click_bus() throws InterruptedException {

		try {
			Thread.sleep(2000);
			driver.findElement(By.id("Bus")).click();
			Thread.sleep(2000);
			driver.findElement(By.xpath("//label[@id='oneway']")).click();
			Thread.sleep(2000);

			WebElement sourceInput = driver.findElement(By.id("dwebSourceInput"));

			sourceInput.clear();

			sourceInput.sendKeys("Pune");
			Thread.sleep(2000);
			driver.findElement(By.xpath("(//div[@class='+2ajg'])[1]")).click();
			Thread.sleep(2000);

			WebElement destinationInput = driver.findElement(By.id("dwebDestinationInput"));
			destinationInput.clear();
			destinationInput.sendKeys("Chandrapur");
			Thread.sleep(2000);
			driver.findElement(By.xpath("(//div[@class='+2ajg'])[1]")).click();
			Thread.sleep(2000);
			driver.findElement(By.xpath("//div[@aria-label='Today']")).click();
			Thread.sleep(2000);

			driver.findElement(By.xpath("//button[normalize-space()='Search Buses']")).click();
			Thread.sleep(10000);
			jse.executeScript("window.scrollBy(0,900)");
			Thread.sleep(2000);
			driver.findElement(By.xpath("//div[normalize-space()='View More(3)']")).click();
            //			driver.findElement(By.id("inputFocus")).sendKeys("Prasanna");
			Thread.sleep(5000);
			driver.findElement(By.xpath("(//div[@class='_0Gfqn UYmgZ'][normalize-space()='Prasanna - Purple Bus'])[1]"))
					.click();
			Thread.sleep(5000);
			jse.executeScript("window.scrollBy(0,-1400)");
		} catch (InterruptedException e) {

			e.printStackTrace();
			throw e;
		}

	}

	@Then("extract the data for paytm travel")
	public void extract_the_data_for_paytm_travel() {
		try {
			// Wait for bus cards to load
			WebDriverWait wait = new WebDriverWait(driver, Duration.ofSeconds(20));
			wait.until(ExpectedConditions.visibilityOfElementLocated(By.cssSelector("div.IHKeM")));

			List<WebElement> buses = driver.findElements(By.cssSelector("div.IHKeM"));
			System.out.println("Total buses found: " + buses.size());

			int count = 1;
			for (WebElement bus : buses) {
				System.out.println("-------------------------------------");
				System.out.println("Bus " + count);

				// Rating
				String rating = "NA";
				try {
					rating = bus.findElement(By.cssSelector("span.QJoiM")).getText();
				} catch (Exception e) {
				}

				// Departure Time
				String departure = "NA";
				try {
					departure = bus.findElement(By.cssSelector("div.wYtCy div._4rWgi")).getText();
				} catch (Exception e) {
				}

				// Arrival Time
				String arrival = "NA";
				try {
					arrival = bus.findElement(By.cssSelector("div.EjC2U div._4rWgi")).getText();
				} catch (Exception e) {
				}

				// Price
				String price = "NA";
				try {
					price = bus.findElement(By.cssSelector("span.A2eT9")).getText();
				} catch (Exception e) {
				}

				System.out.println("Rating: " + rating);
				System.out.println("Departure: " + departure);
				System.out.println("Arrival: " + arrival);
				System.out.println("Price: " + price);

				count++; // increment bus number
			}

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}