package ads.assignment3;

import java.util.List;

/**
 * Tester for Part 2 of lab assignment 3
 * Receives the file name through the command line
 *
 * @param args[0] First and only command line argument must be the name of the text file describing products
 * @author Course Faculty

 */

public class Tester2 {
    public static void main(String[] args) {
    	List<Appliance> products = ApplianceReader.readAppliances( args[0] );
    	for (Appliance p : products) { 
    		System.out.println(">> " + p ); 
    	}
    	
    	// last test of equality
    	Appliance wash1 = new Washer("Indesit", "XWE 91483 X", 329.0,
				EnergyEfficiency.A, new Dimension(59.5, 60.5, 85.0), 72, 9.5, 1500);
        Appliance frigo1 = new Refrigerator("Bosch", "KGN39VW21", 599.0,
				EnergyEfficiency.A, new Dimension(60, 65, 201), 83.0, true);
    }
}