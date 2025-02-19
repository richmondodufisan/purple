#include "IncompressibilityConstraint.h"
#include "Material.h"
#include "MooseMesh.h"
#include "MooseVariable.h"
#include "SystemBase.h"
#include "NonlinearSystem.h"

#include <cmath>

#include "libmesh/quadrature.h"
#include "libmesh/fe_interface.h"
#include "libmesh/string_to_enum.h"
#include "libmesh/quadrature_gauss.h"
#include "libmesh/quadrature.h"

registerMooseObject("purpleApp", IncompressibilityConstraint);

InputParameters
IncompressibilityConstraint::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Kernel that calculates the value of p and enforces incompressibility");

  params.addParam<std::string>("base_name", "Material property base name");
  

  return params;
}


IncompressibilityConstraint::IncompressibilityConstraint(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    _deformation_gradient(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient"))
{
}

ADReal
IncompressibilityConstraint::computeQpResidual()
{
  auto F = _deformation_gradient[_qp];
  
  auto J = F.det();
  
  // auto residual = std::log(J) * _test[_i][_qp];

  if (J <= 0.0) {
	  
	  std::cout << "F = " << F << " at location: " << _q_point[_qp] << std::endl;
	  
	  std::cout << "negative jacobian!!! J = " << J << "  at location: " << _q_point[_qp] << std::endl;
      // J = eps;  // Prevent NaN by ensuring J is never zero or negative
  }

  auto residual = std::log(J) * _test[_i][_qp];
  
  return  residual;
}