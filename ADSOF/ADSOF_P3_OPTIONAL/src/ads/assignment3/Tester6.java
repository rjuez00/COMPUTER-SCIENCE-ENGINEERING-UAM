package ads.assignment3;

/**
 * 
 * Tester for Part 2 of lab assignment 3
 * Receives the file name through the command line
 *
 * @param args[0] First and only command line argument must be the name of the text file describing products
 * @author Course Faculty

 */

public class Tester6 {
    public static void main(String[] args) {
    	Stock stock = Stock.getInstance();
    	
    	Appliance curved = new CurvedTelevision("Curvada", "4K Oro", 1893.30,
					EnergyEfficiency.C, 56, 215, new Dimension(100,100,100));

	    Appliance tv1 = new Television("Samsung", "8K Negro", 1900.00,
					EnergyEfficiency.A, 48);

	    Appliance wash1 = new Washer("Frigopie", "XWE xRay X", 501.00,
					EnergyEfficiency.A, new Dimension(59.5, 60.5, 85.0), 72, 9.5, 1500);
	    
	    Appliance wash2 = new Washer("Frigopie", "XWE xRay X", 501.00,
				EnergyEfficiency.A, new Dimension(59.5, 60.5, 85.0), 72, 9.5, 1200);
		//New appliances received by the manufacturer
	    stock.addStock(tv1);
	    stock.addStock(tv1);
	    stock.addStock(wash1);
	    stock.addStock(wash2);
	    
	    System.out.println("ALL STOCK:");
	    System.out.print(stock.showStock());
	    
	    System.out.println("TV STOCK:");
	    System.out.print(stock.showStock(Television.class));
	    System.out.println("WASHER STOCK:");
	    System.out.print(stock.showStock(Washer.class));
	    System.out.println("REFRIGERATOR STOCK:");
	    System.out.print(stock.showStock(Refrigerator.class));
	    System.out.println("END OF BASELINE STOCK:\n");

	    
	    //New sales by clients. Returned objects get in the stock catalog for re-selling them
	    Sale[] sales = new Sale[5];
	    sales[0] = new Sale(tv1, curved);
	    System.out.println("CATALOGUE AFTER FIRST Samsung TV SALE (returns a curved tv):");
	    System.out.print(stock.showStock());
	    
	    sales[1] = new HomeDeliverySale(tv1);
	    System.out.println("CATALOGUE AFTER SECOND Samsung TV SALE (returns nothing):");
	    System.out.print(stock.showStock());

	    Sale.cancel();
	    System.out.println("PREVIOUS Samsung SALE CANCELLED:");
	    System.out.print(stock.showStock());

	    sales[4] = new CanaryIslandsHomeDeliverySale(wash2);
	    System.out.println("CATALOGUE AFTER WASHER TV SALE (returns nothing):");
	    System.out.print(stock.showStock());
	    
	    
	    
	    
	    
	    
    	   
    	
    }
}
