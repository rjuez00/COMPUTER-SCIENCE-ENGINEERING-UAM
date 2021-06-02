package units;

/**
*
* Ennumeration for unit types
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
public enum Quantity {
	
	/** Length. */
	L, 
	/** Time. */
	t,
	/** Length/Time. */
	Ltd,
	/** Time/Length. */
	tLd,
	/** Length*Time. */
	Ltm,
	/** Time*Length. */
	tLm;

	static Quantity composite(Quantity a, Quantity b, Operator o) {
		if(a==L && b==t) {
			if(o == Operator.DIV) return Ltd;
			else return Ltm;
		}
		else {
			if(o== Operator.DIV) return tLd;
			else return tLm;
		}
	}
}


