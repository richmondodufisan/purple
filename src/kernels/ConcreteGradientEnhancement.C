#include "ConcreteGradientEnhancement.h"
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

registerMooseObject("purpleApp", ConcreteGradientEnhancement);

InputParameters
ConcreteGradientEnhancement::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Calculate concrete Gradient Enhancement");

  params.addParam<std::string>("base_name", "Material property base name");

  return params;
}


ConcreteGradientEnhancement::ConcreteGradientEnhancement(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
	
	_ndisp(coupledComponents("displacements")),
    _disp_var(_ndisp),
	
    /// Gets properties from material interface
    _len_scale(getADMaterialPropertyByName<Real>("nonlocal_radius")),
	_kappa(getADMaterialPropertyByName<Real>("kappa"))
	
	
{
}

ADReal 
ConcreteGradientEnhancement::computeQpResidual()
{
  
  // Implement residual here
  const auto & dNA_dx = _grad_test[_i][_qp];
  const auto & NA = _test[_i][_qp];

  const auto & k_bar = _u[_qp];
  const auto & k_bar_grad = _grad_u[_qp];
  const auto & k_loc = _kappa[_qp];

  const auto & len_scale = _len_scale[_qp];


  ADReal term3 = 0.0;
  for (unsigned int i = 0; i < 3; ++i)
  {
  	term3 += (len_scale*len_scale) * dNA_dx(i) * k_bar_grad(i);
  }

  return (NA * k_bar) - (NA * k_loc) + term3;
}
    