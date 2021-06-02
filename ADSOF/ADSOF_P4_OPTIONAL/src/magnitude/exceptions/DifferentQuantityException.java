package magnitude.exceptions;
import units.IPhysicalUnit;

/**
*
* Class for declaring a new type of Quantity Exception.
*
* @author Rodrigo Juez - rodrigo.juezh@estudiante.uam.es and Juan Luis Sanz - juanluis.sanzc@estudiante.uam.es
*
*/
@SuppressWarnings("serial")
public class DifferentQuantityException extends QuantityException {

    /**
     * Instantiates a new different quantity exception.
     *
     * @param first unit type
     * @param second unit type
     */
    public DifferentQuantityException(IPhysicalUnit firstype, IPhysicalUnit secondtype) {
        super(firstype, secondtype);
    }

    /**
     * ToString.
     *
     * @return the string
     */
    @Override
    public String toString() {
		return "Quantities " + secondtype.getQuantity() +" and " + firstype.getQuantity() + " are not compatible\n";
    }

}