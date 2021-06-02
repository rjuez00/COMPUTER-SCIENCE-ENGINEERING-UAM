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
    	
    }
}
