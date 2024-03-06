#include "ConcreteGradientDamageMomentum.h"
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

registerMooseObject("purpleApp", ConcreteGradientDamageMomentum);

InputParameters
ConcreteGradientDamageMomentum::validParams()
{
  InputParameters params = ADKernel::validParams();
  params.addClassDescription("Calculate Erosion Momentum Balance");

  params.addRequiredParam<unsigned int>("component_disp",
                                        "An integer corresponding to the direction "
                                        "the variable this kernel acts in. (0 for x, "
                                        "1 for y, 2 for z)");

  params.addRequiredCoupledVar("displacements",
                               "The string of displacements suitable for the problem statement");
  params.addParam<std::string>("base_name", "Material property base name");
  

  return params;
}


ConcreteGradientDamageMomentum::ConcreteGradientDamageMomentum(const InputParameters & parameters)
  : DerivativeMaterialInterface<ADKernel>(parameters),

    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),

    _stress(getADMaterialPropertyByName<RankTwoTensor>(_base_name + "stress")),
    _cto(getADMaterialPropertyByName<RankFourTensor>(_base_name + "elasticity_tensor")),
    _strain(getADMaterialPropertyByName<RankTwoTensor>(_base_name + "mechanical_strain")),


    _component_disp(getParam<unsigned int>("component_disp")),
    _ndisp(coupledComponents("displacements")),
    _disp_var(_ndisp),


	_D(getADMaterialPropertyByName<Real>("damage"))
{
}

ADReal
ConcreteGradientDamageMomentum::computeQpResidual()
{
  n_dim = 3;
  auto i = _component_disp;

  auto grad_NA = _grad_test[_i][_qp];
  auto stress = _stress[_qp];

  auto D = _D[_qp];

  ADReal stressum = 0.0;

  for (unsigned int k=0; k<n_dim; ++k)
  {
	stressum += stress(i,k) * grad_NA(k);
  }

  auto residual = (1-D)*stressum;
  
  return  residual;
}
