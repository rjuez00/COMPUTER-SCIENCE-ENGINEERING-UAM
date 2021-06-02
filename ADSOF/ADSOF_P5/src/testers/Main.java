package testers;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.List;
import java.util.Calendar;
import java.util.concurrent.TimeUnit;

import rules.*;

public class Main {
	public static void main(String...args) throws ParseException{
		SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
		RuleSet<Product> rs = new RuleSet<Product>(); // A set of rules applicable to Products
		rs.add(
				Rule.<Product>rule("r1", "10% discount on products with an expiration date close or past").
				when(pro -> Product.getDateDiff(Calendar.getInstance().getTime(), pro.getExpiration(), TimeUnit.DAYS) < 2 ).
				exec(pro -> pro.setPrice(pro.getPrice()-pro.getPrice()*0.1))
				).add(
						Rule.<Product>rule("r2", " Discount on products with price more than 10 euros").
						when(pro -> pro.getPrice() > 10).
						exec(pro -> pro.setPrice(pro.getPrice()-pro.getPrice()*0.05))
						);
		List<Product> str = Arrays.asList( new Product(10, sdf.parse("15/04/2020")), // parses a date
				new Product(20, sdf.parse("20/03/2021")));
		
		rs.setExecContext(str); // indicates that the rule set rs will be executed over str
		rs.process(); // we execute the rule set
		System.out.println(str); // prints str
	}
}