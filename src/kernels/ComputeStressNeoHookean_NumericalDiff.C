#include "ComputeStressNeoHookean_NumericalDiff.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeStressNeoHookean_NumericalDiff);

InputParameters
ComputeStressNeoHookean_NumericalDiff::validParams()
{
  InputParameters params = ComputeLagrangianStressPK1::validParams();
  params.addClassDescription("send PK1 Stress for Neo Hookean Model to system");

  return params;
}

ComputeStressNeoHookean_NumericalDiff::ComputeStressNeoHookean_NumericalDiff(const InputParameters & parameters)
  : ComputeLagrangianStressPK1(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
	
	_PK1_in(getMaterialPropertyByName<RankTwoTensor>(_base_name + "PK1")),	// this is the stress
	_dPdF_in(getMaterialPropertyByName<RankFourTensor>(_base_name + "dPK1_dF")) //this is the tangent operator


{
}


void
ComputeStressNeoHookean_NumericalDiff::computeQpPK1Stress()
{
	_pk1_stress[_qp] = _PK1_in[_qp];
	
	_pk1_jacobian[_qp] = _dPdF_in[_qp];
	
}


