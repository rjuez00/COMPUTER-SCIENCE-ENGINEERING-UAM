package ads.assignment3;
import java.io.*;
import java.util.*;


/**
*
* Class for reading a formatted file
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class ApplianceReader {

	/**
	 * reads a formatted file and returns an arraylist
	 * @param name
	 * @return
	 */
	public static List<Appliance> readAppliances(String name){
		//we could use a set but a list retains order
		List <Appliance> appl = new ArrayList <Appliance>();
		try {	
			BufferedReader buffer = new BufferedReader(
									  new InputStreamReader(
										new FileInputStream(name)));
					
			String line;
			
			System.out.println("Duplicated not added:");
			
		    while ((line = buffer.readLine()) != null) {
		    	String[] arguments = line.split("=");
		    	
		    	
			    Appliance myapp = null;
			    
		    	if(arguments.length == 5) 
		    		myapp = parseTV(arguments);
		    	
		    	else if(arguments.length == 9 || arguments.length == 10 || arguments.length == 8) {
		    		if(arguments.length == 9 && (arguments[8].compareTo("NoFrost") == 0 || arguments[8].compareTo("Frost") == 0)) {
			    		myapp = parseRefrigerator(arguments);
		    		}
		    		else {
			    		myapp = parseWasher(arguments);
		    		}
		    	}
		    	
		    	
		    	
		    	
		    	if(appl.contains(myapp) == false) 
		    		appl.add(myapp);
		    	else 
		    		System.out.println(myapp);
		    }
		    buffer.close();
	 } catch(IOException e) {
		 System.out.println("ERROR IN READ_LINE");
		 return null;
	 	}
	
	 return appl;
	}	
	
	/**
	 * parses the energy readed from the string argument 
	 * @param argument
	 * @return an EnergyEffiency variable from the string
	 */
	private static EnergyEfficiency parseEnergy(String argument) {
		
		EnergyEfficiency currentenergy;
		if(argument.charAt(0) == 'A') 				currentenergy = EnergyEfficiency.A;
		else if(argument.charAt(0) == 'B') 			currentenergy = EnergyEfficiency.B;
		else if(argument.charAt(0) == 'C') 			currentenergy = EnergyEfficiency.C;
		else if(argument.charAt(0) == 'D') 			currentenergy = EnergyEfficiency.D;
		else if(argument.compareTo("UNKNOWN") == 0) currentenergy = EnergyEfficiency.UNKNOWN;
		else {
			currentenergy = null;
			throw new IllegalArgumentException("Not an EnergyEfficiency readed!");
		}
		return currentenergy;
	}
	/**
	 * parses the tv readed from the string argument 
	 * @param arguments
	 * @return a tv object
	 */
	private static Television parseTV (String[] arguments) { 
		double argument2 = -1;
		int argument4 = -1;
		try {
			argument2 = Double.parseDouble(arguments[2]);
			argument4 = Integer.parseInt(arguments[4]);
		} catch(NumberFormatException e) {
			System.out.println("not a integer/double passed");
			return null;
		}
		
		Television myapp = new Television(arguments[0], arguments[1], argument2, parseEnergy(arguments[3]) , argument4);	
		return myapp;
	}
	/**
	 * parses the Refrigerator readed from the string argument 
	 * @param arguments
	 * @return a refrigerator object
	 */
	private static Refrigerator parseRefrigerator (String[] arguments) { 
		double argument2 = -1, argument5 = -1, argument7 = -1, argument6 = -1, argument4 = -1;
		boolean nofrost = false;
		try {
			argument2 = Double.parseDouble(arguments[2]);
			argument5 = Double.parseDouble(arguments[5]);
			argument4 = Double.parseDouble(arguments[4]);
			argument7 = Double.parseDouble(arguments[7]);
			argument6 = Double.parseDouble(arguments[6]);
		} catch(NumberFormatException e) {
			System.out.println("not a integer/double passed");
			return null;
		}
		
		if( arguments[8].compareTo("NoFrost") == 0) nofrost = true;
		Dimension dim = new Dimension(argument4, argument5, argument6);
		Refrigerator myapp = new Refrigerator(arguments[0], arguments[1], argument2, parseEnergy(arguments[3]), dim, argument7, nofrost);
		return myapp;
	}
	/**
	 * parses the washer readed from the string argument 
	 * @param arguments
	 * @return a Washer object
	 */
	private static Washer parseWasher(String[] arguments) {
		double argument2 = -1, argument5 = -1, argument7 = -1, argument8=-1, argument6 = -1, argument4 = -1;
		int argument9= -1;
		Washer myapp = null;
		if(arguments.length == 10) {
			try {
				argument9 = Integer.parseInt  (arguments[9]);
				argument8 = Double.parseDouble(arguments[8]);
				argument2 = Double.parseDouble(arguments[2]);
				argument5 = Double.parseDouble(arguments[5]);
				argument4 = Double.parseDouble(arguments[4]);
				argument7 = Double.parseDouble(arguments[7]);
				argument6 = Double.parseDouble(arguments[6]);
			} catch(NumberFormatException e) {
				System.out.println("not a integer/double passed");
				return null;
			}
			Dimension dim = new Dimension(argument4, argument5, argument6);
			myapp = new Washer(arguments[0], arguments[1], argument2, parseEnergy(arguments[3]), dim, argument7, argument8, argument9);      	
		}
		
		else if(arguments.length == 8){
			try {
				argument2 = Double.parseDouble(arguments[2]);
				argument5 = Double.parseDouble(arguments[5]);
				argument4 = Double.parseDouble(arguments[4]);
				argument7 = Double.parseDouble(arguments[7]);
				argument6 = Double.parseDouble(arguments[6]);
			} catch(NumberFormatException e) {
				System.out.println("not a integer/double passed");
				return null;
			}
			
			Dimension dim = new Dimension(argument4, argument5, argument6);
			myapp = new Washer(arguments[0], arguments[1], argument2, parseEnergy(arguments[3]), dim, argument7);
		}
		
		if(arguments.length == 9) {
			try {
				argument8 = Double.parseDouble(arguments[8]);
				argument2 = Double.parseDouble(arguments[2]);
				argument5 = Double.parseDouble(arguments[5]);
				argument4 = Double.parseDouble(arguments[4]);
				argument7 = Double.parseDouble(arguments[7]);
				argument6 = Double.parseDouble(arguments[6]);
			} catch(NumberFormatException e) {
				System.out.println("not a integer/double passed");
				return null;
			}
			
			if(argument8 > 200) { //if is more than 200 then is rpm this was selected as the teacher told us to
				Dimension dim = new Dimension(argument4, argument5, argument6);
				myapp = new Washer(arguments[0], arguments[1], argument2, parseEnergy(arguments[3]), dim, argument7, -1, (int)argument8);      	
			}
			else {
				Dimension dim = new Dimension(argument4, argument5, argument6);
				myapp = new Washer(arguments[0], arguments[1], argument2, parseEnergy(arguments[3]), dim, argument7, argument8, -1);      	
			}
		}
		
		
		
		return myapp;
	}
}