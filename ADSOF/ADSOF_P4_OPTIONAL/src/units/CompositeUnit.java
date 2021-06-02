/**
 * 
 */
package units;

import java.util.ArrayList;

import magnitude.Magnitude;
import magnitude.exceptions.QuantityException;
import metricSystems.CompositeMetricSystem;
import metricSystems.IMetricSystem;

/**
 * @author Rodrigo
 *
 */
public class CompositeUnit implements ICompositeUnit {
	PhysicalUnit left;
	PhysicalUnit right;
	Operator operator;
	Quantity quantity;
	public CompositeUnit(PhysicalUnit left, Operator operator, PhysicalUnit right) {
		this.left=left;
		this.right=right;
		this.operator=operator;
	}

	@Override
	public Operator getOperator() {
		return this.operator;
	}

	@Override
	public IPhysicalUnit getLeftUnit() {
		return this.left;
	}

	@Override
	public IPhysicalUnit getRightUnit() {
		return this.right;
	}

	@Override
	public boolean canTransformTo(IPhysicalUnit u) {
		if(u.getClass() != this.getClass()) return false;
		ICompositeUnit other = (ICompositeUnit)u;
		if(this.getLeftUnit().canTransformTo(other.getLeftUnit()) && this.getRightUnit().canTransformTo(other.getRightUnit()) == true) return true;
		return false;
	}

	@Override
	public double transformTo(double d, IPhysicalUnit u) throws QuantityException {
		ICompositeUnit other = (ICompositeUnit)u;
		
		Magnitude leftmag = new Magnitude(1, this.getLeftUnit());
		Magnitude rightmag = new Magnitude(1, this.getRightUnit());

		if(operator == Operator.DIV) return d * leftmag.transformTo(other.getLeftUnit()).getValue()/ rightmag.transformTo(other.getRightUnit()).getValue();
		
		if(operator == Operator.MUL) return d * leftmag.transformTo(other.getLeftUnit()).getValue()* rightmag.transformTo(other.getRightUnit()).getValue();

		return 0;
	}

	@Override
	public Quantity getQuantity() {
		return Quantity.composite(this.getLeftUnit().getQuantity(), this.getRightUnit().getQuantity(), this.getOperator());
	}

	@Override
	public String abbrev() {
		return this.getLeftUnit().abbrev() + " / " + this.getRightUnit().abbrev();
	}

	@Override
	public IMetricSystem getMetricSystem() {
		ArrayList<IPhysicalUnit> allunits = new ArrayList<>();
		allunits.addAll(this.getLeftUnit().getMetricSystem().units());
		allunits.addAll(this.getRightUnit().getMetricSystem().units());

		return new CompositeMetricSystem(this, allunits);
	}
	@Override
	public String toString() {
		return this.abbrev();
	}



}
