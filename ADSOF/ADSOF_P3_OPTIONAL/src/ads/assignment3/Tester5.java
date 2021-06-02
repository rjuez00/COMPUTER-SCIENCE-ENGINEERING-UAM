package ads.assignment3;

/**
 * Tester for Part 2 of lab assignment 3
 * Receives the file name through the command line
 *
 * @param args[0] First and only command line argument must be the name of the text file describing products
 * @author Course Faculty

 */

public class Tester5 {
    public static void main(String[] args) {
    	Appliance curved = new CurvedTelevision("Curvada", "Art 48 4K Oro", 1893.30,
					EnergyEfficiency.C, 56, 215, new Dimension(100,100,100));
    	Appliance notcurved = new Television("NOCurvada", "Art 56 8K Oro", 1893.30,
				EnergyEfficiency.C, 56);
    	
	    Appliance tv1 = new Television("Loewe", "Art 48 4K Plata", 1699.00,
					EnergyEfficiency.A, 48);
	    Appliance tv2 = new Television("LG", "32LF592U", 271.92,
					EnergyEfficiency.C, 32);
	    Appliance wash1 = new Washer("Indesit", "XWE 91483 X", 329.0,
					EnergyEfficiency.A, new Dimension(59.5, 60.5, 85.0), 72, 9.5, 1500);
	    Appliance frigo1 = new Refrigerator("Bosch", "KGN39VW21", 599.0,
					EnergyEfficiency.A, new Dimension(60, 65, 201), 83.0, true);
			
	    Sale[] sales = new Sale[9];
	    sales[0] = new Sale(tv1);
	    sales[1] = new HomeDeliverySale(tv1);
	    sales[2] = new Sale(tv1, 
	                       new Washer("Superkin", "", 0.0, EnergyEfficiency.UNKNOWN, 
	                                  new Dimension(59.5, 60.5, 85.0), 100)); // no load nor RPM
	    sales[3] = new HomeDeliverySale(wash1, frigo1);
	    sales[4] = new Sale(tv2, 
	                       new Television("Telefunken", "", 0.0, EnergyEfficiency.D, 32));
	    sales[5] = new HomeDeliverySale(wash1, tv2);
	    sales[6] = new HomeDeliverySale(notcurved);
	    sales[7] = new HomeDeliverySale(curved);
	    
	    sales[8] = new CanaryIslandsHomeDeliverySale(curved);
	    
	    for (Sale s : sales) 
	    	System.out.print(s.getTicket());	
    	   
    	
    }
}
