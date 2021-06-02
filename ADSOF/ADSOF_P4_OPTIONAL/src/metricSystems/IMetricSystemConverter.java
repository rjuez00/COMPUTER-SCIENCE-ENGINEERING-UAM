package metricSystems;


import magnitude.IMagnitude;
import magnitude.exceptions.UnknownUnitException;
import units.IPhysicalUnit;

public interface IMetricSystemConverter {
	IMetricSystem sourceSystem();
	IMetricSystem targetSystem();
	IMagnitude transformTo(IMagnitude from, IPhysicalUnit to) throws UnknownUnitException;
	IMetricSystemConverter reverse();
}