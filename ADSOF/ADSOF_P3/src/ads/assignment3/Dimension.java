package ads.assignment3;

/**
*
* 3 dimensional values, used for calculating volumes on other classes
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*
*/
public class Dimension {
	public double sizex;
	public double sizey;
	public double sizez;
	
	/**
	 * 3 dimensional constructor
	 * @param sizex
	 * @param sizey
	 * @param sizez
	 */
	public Dimension(double sizex, double sizey, double sizez) {
		this.sizex = sizex;
		this.sizey = sizey;
		this.sizez = sizez;
	}

	public String toString() {
		return "x:" + sizex + " y:" + sizey + " z:" + sizez;
	}
	
	@Override
    public boolean equals(Object obj) { 
		if (obj == null || obj.getClass() != this.getClass()) return false;
		Dimension other = (Dimension) obj;
		
		return (this.sizex == other.sizex) && (this.sizey == other.sizey) && (this.sizez == other.sizez) ;
	}
	
	@Override
	public int hashCode() {
		return (int)this.sizex* (int)this.sizey* (int)this.sizez;
	}
}
