#include "PressureStabilizationConstraint.h"
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

registerMooseObject("purpleApp", PressureStabilizationConstraint);

InputParameters
PressureStabilizationConstraint::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Kernel that stabilizes the incompressibility constraint globally");

  params.addParam<std::string>("base_name", "Material property base name");
  
  params.addRequiredCoupledVar("pressure", "the pressure variable");

  return params;
}


PressureStabilizationConstraint::PressureStabilizationConstraint(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    _pressure(coupledValue("pressure"))
{
}

ADReal
PressureStabilizationConstraint::computeQpResidual()
{
  
  auto residual = _pressure[_qp] * _test[_i][_qp];
  
  return  residual;
}



