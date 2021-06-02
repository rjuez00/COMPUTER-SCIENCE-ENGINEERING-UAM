package test;

import units.CompositeUnit;
import units.Operator;
import magnitude.Magnitude;
import magnitude.exceptions.QuantityException;
import metricSystems.imperial.length.ImperialLengthMetricSystem;
import metricSystems.si.length.SiLengthMetricSystem;
import metricSystems.si.length.converters.SiLength2ImperialConverter;
import metricSystems.si.time.SiTimeMetricSystem;

public class CompositeTest {
	public static void main(String[] args) throws QuantityException{
		SiLengthMetricSystem.registerConverter(new SiLength2ImperialConverter());
		
		Magnitude velocSI = new Magnitude(10, new CompositeUnit(SiLengthMetricSystem.METER, Operator.DIV, SiTimeMetricSystem.SECOND));
		Magnitude velocImp = new Magnitude(0, new CompositeUnit(ImperialLengthMetricSystem.MILE, Operator.DIV, SiTimeMetricSystem.HOUR));
		Magnitude velocSI2 = new Magnitude(0, new CompositeUnit(SiLengthMetricSystem.KILOMETER, Operator.DIV, SiTimeMetricSystem.HOUR));
		System.out.println(velocSI);
		System.out.println(velocImp);
		System.out.println(velocImp.add(velocSI));	// implica convertir m/s a millas/hora
		System.out.println(velocSI2.add(velocSI));	// implica convertir m/s a km/hora	
	}
}
