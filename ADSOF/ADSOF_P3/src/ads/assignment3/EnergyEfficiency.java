package ads.assignment3;

/**
 * levels of energy effiency
 *
 */
public enum EnergyEfficiency{
	/**
	 * unknown effiency
	 */
	UNKNOWN(-1), 
	/**
	 * best possible rating
	 */
	A(0), 
	/**
	 * medium high rating 
	 */
	B(1), 
	/**
	 * medium low rating
	 */
	C(2), 
	/**
	 * lowest possible rating
	 */
	D(3);
	private final int value; // controlled internal value
	
	/**
	 * assigns value
	 * @param d
	 */
	private EnergyEfficiency(int d) { value = d; } // private constructor
	/**
	 * returns value to compare different energies
	 * @return integer with such value (highest number = worst, -1 = unknown)
	 */
	public int value() { return value; }
}