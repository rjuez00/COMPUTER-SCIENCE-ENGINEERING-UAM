/**
 * 
 */
package units;


public interface ICompositeUnit extends IPhysicalUnit{
	Operator getOperator();
	IPhysicalUnit getLeftUnit();
	IPhysicalUnit getRightUnit();
}
