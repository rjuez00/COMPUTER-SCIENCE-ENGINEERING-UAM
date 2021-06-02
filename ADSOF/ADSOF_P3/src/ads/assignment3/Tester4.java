package ads.assignment3;

/**
 * Tester for Part 4 of lab assignment 3
 * @author Course Faculty
 */
public class Tester4 {	
	public static void main(String[] args) {		
		// first execute tester1 to load appliances and sales
		Tester1.main(null);  
		
		System.out.println( Sale.salesSummary() );
		System.out.println( Sale.last().getTicket() );
		
		Sale cancelled = Sale.cancel();  // cancell the last sale    
		System.out.println("Sale cancelled:\n" + cancelled.getTicket());
		
		Sale.cancel();  // cancel another sale
		// eliminado por redundante    Venta.resumenVentas(); // sin las dos ultimas ventas		
		System.out.println( Sale.salesSummary(500) ); // without last two sales nor the one with price < 500
		System.out.println( Sale.salesSummary("Indes") ); // only sales not cancelled and with brand Indesit

	}
}
