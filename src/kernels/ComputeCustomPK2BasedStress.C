#include "ComputeCustomPK2BasedStress.h"
#include <Eigen/Dense>
#include <cmath>

registerMooseObject("purpleApp", ComputeCustomPK2BasedStress);

InputParameters
ComputeCustomPK2BasedStress::validParams()
{
  InputParameters params = ComputeLagrangianStressPK2::validParams();
  params.addClassDescription("send PK2 Stress for Neo Hookean Model to system");

  return params;
}

ComputeCustomPK2BasedStress::ComputeCustomPK2BasedStress(const InputParameters & parameters)
  : ComputeLagrangianStressPK2(parameters),

	/// Base name to prefix material properties
	_base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
	
	_PK2_in(getMaterialPropertyByName<RankTwoTensor>(_base_name + "PK2")),	// this is the stress
	_dPdE_in(getMaterialPropertyByName<RankFourTensor>(_base_name + "dPK2_dE")) //this is the tangent operator


{
}


void
ComputeCustomPK2BasedStress::computeQpPK2Stress()
{
	// _S and _C are the names of the stress and tangent in the class it inherits from
	
	_S[_qp] = _PK2_in[_qp];
	
	_C[_qp] = _dPdE_in[_qp];
	
}


