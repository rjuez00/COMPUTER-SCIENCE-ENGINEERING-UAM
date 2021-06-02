package testers;

import java.util.ArrayList;
import java.util.Date;
import java.util.concurrent.TimeUnit;

import rules.triggers.Observed;
import rules.triggers.TriggeredRule;

class Product implements Observed<Product>{ // A sample class to test the rules
	private double price;
	private Date expiration; // A better option is to use Calendar
	private ArrayList<TriggeredRule<Product>> triggerers = new ArrayList<>();
	
	public Product(double p, Date c) {
		this.price = p;
		this.expiration = c;
	}

	public double getPrice() {
		return this.price;
	}

	public void setPrice(double p) {
		if(triggerers.size() != 0)
			triggerers.stream().filter( (TriggeredRule<Product> o) -> o.getWhen().test(this) ).forEach((TriggeredRule<Product> o) -> o.getExec().accept(this));;
		
				
		this.price = p;
	}

	public Date getExpiration() {
		return this.expiration;
	}

	public static long getDateDiff(Date date1, Date date2, TimeUnit timeUnit) {
		long diffInMillies = date2.getTime() - date1.getTime();
		return timeUnit.convert(diffInMillies, TimeUnit.MILLISECONDS);
	}

	@Override
	public String toString() {
		return this.price + ", expiration: " + this.expiration;
	}

	@SuppressWarnings("unchecked")
	@Override
	public void addTriggerer(TriggeredRule<?> triggerer) {
		triggerers.add((TriggeredRule<Product>)triggerer);
	}
}
