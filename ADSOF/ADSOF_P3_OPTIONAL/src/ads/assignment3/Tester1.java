package ads.assignment3;

/**
 * Tester for Part 1 of lab assignment 3
 * @author Course Faculty
 */
public class Tester1 {
	  public static void main(String[] args) {
	    Appliance tv1 = new Television("Loewe", "Art 48 4K Plata", 1699.00,
					EnergyEfficiency.A, 48);
	    Appliance tv2 = new Television("LG", "32LF592U", 271.92,
					EnergyEfficiency.C, 32);
	    Appliance wash1 = new Washer("Indesit", "XWE 91483 X", 329.0,
					EnergyEfficiency.A, new Dimension(59.5, 60.5, 85.0), 72, 9.5, 1500);
	    Appliance frigo1 = new Refrigerator("Bosch", "KGN39VW21", 599.0,
					EnergyEfficiency.A, new Dimension(60, 65, 201), 83.0, true);
			
	    Sale[] sales = new Sale[6];
	    sales[0] = new Sale(tv1);
	    sales[1] = new HomeDeliverySale(tv1);
	    sales[2] = new Sale(tv1, 
	                       new Washer("Superkin", "", 0.0, EnergyEfficiency.UNKNOWN, 
	                                  new Dimension(59.5, 60.5, 85.0), 100)); // no load nor RPM
	    sales[3] = new HomeDeliverySale(wash1, frigo1);
	    sales[4] = new Sale(tv2, 
	                       new Television("Telefunken", "", 0.0, EnergyEfficiency.D, 32));
	    sales[5] = new HomeDeliverySale(wash1, tv2);
	    for (Sale s : sales) 
	    	System.out.print(s.getTicket());		
	 }
}

