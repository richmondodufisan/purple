#include "TLStressDivergenceNearlyIncompressible.h"
#include "DerivativeMaterialInterface.h"

registerMooseObject("purpleApp", TLStressDivergenceNearlyIncompressible);

InputParameters
TLStressDivergenceNearlyIncompressible::validParams()
{
  InputParameters params = Kernel::validParams();
  params.addClassDescription("Divergence of stress tensor");
  
  
  
  params.addParam<std::string>("base_name", "Material property base name");
  params.addRequiredParam<unsigned int>("component",
                                        "An integer corresponding to the direction "
                                        "the variable this kernel acts in. (0 for x, "
                                        "1 for y, 2 for z)");
  params.addRequiredCoupledVar("displacements",
                               "The string of displacements suitable for the problem statement");


  ////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
  params.addRequiredParam<Real>("kappa", "bulk modulus/penalty parameter");
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  return params;
}

TLStressDivergenceNearlyIncompressible::TLStressDivergenceNearlyIncompressible(const InputParameters & parameters)
  : DerivativeMaterialInterface<Kernel>(parameters),
  
  
    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
	
	
	
    _P(getMaterialPropertyByName<RankTwoTensor>(_base_name + "pk1_stress")),
    _dP_dF(getMaterialPropertyByName<RankFourTensor>(_base_name + "pk1_jacobian")),
	_F(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),



    _component(getParam<unsigned int>("component")),
    _ndisp(coupledComponents("displacements")),
    _disp_var(_ndisp),
	
	
	////////////////////////// ADDED STUFF //////////////////////////////////////////////////////////////////////////////////////////////////////// 
    _kappa(getParam<Real>("kappa")) 
	////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




{
  // Do the vector coupling of the displacements
  for (unsigned int i = 0; i < _ndisp; i++)
    _disp_var[i] = coupled("displacements", i);

  // We need to use identical discretizations for all displacement components
  auto order_x = getVar("displacements", 0)->order();
  for (unsigned int i = 1; i < _ndisp; i++)
  {
    if (getVar("displacements", i)->order() != order_x)
      mooseError("The Lagrangian StressDivergence kernels require equal "
                 "order interpolation for all displacements.");
  }
}

Real
TLStressDivergenceNearlyIncompressible::computeQpResidual()
{
  // We abandon MOOSE's 'creative' naming scheme here:
  //
  // Node index A = _i
  // direction test function i = _component
  //

  const auto & dNA_dX = _grad_test[_i][_qp];
  const auto & NA = _test[_i][_qp];
  const auto & i = _component;
  
  
  const auto & P = _P[_qp];
  const auto & F = _F[_qp];
  const auto & F_inv = F.inverse();
  const auto & Jac = F.det();
  
  const auto & kappa = _kappa;
  
  
  Real residual_Ai = 0.0;
  
  for (int J = 0;  J < _ndisp; ++J)
  {
    // No incompressibility enforced
	// residual_Ai += P(i, J) * dNA_dX(J);
	
	// Near Incompressibility ln(J)
	residual_Ai += (P(i, J) + (kappa * std::log(Jac) * F_inv(J, i))) * dNA_dX(J);
	
  }  



  return residual_Ai;
}

Real
TLStressDivergenceNearlyIncompressible::computeQpJacobian()
{
  const auto ivar = _var.number();

  for (unsigned int i = 0; i < _ndisp; ++i)
    if (ivar == _disp_var[i])
      return computeQpJacobianDisplacement(_component, _component);

  mooseError("Jacobian for unknown variable requested");
  return 0.0;
}

Real
TLStressDivergenceNearlyIncompressible::computeQpOffDiagJacobian(unsigned int jvar)
{
  for (unsigned int j = 0; j < _ndisp; ++j)
    if (jvar == _disp_var[j])
      return computeQpJacobianDisplacement(_component, j);

  mooseError("Jacobian for unknown variable requested");
  return 0.0;
}

Real
TLStressDivergenceNearlyIncompressible::computeQpJacobianDisplacement(unsigned int comp_i, unsigned int comp_k)
{

  const auto & dNA_dX = _grad_test[_i][_qp];
  const auto & NA = _test[_i][_qp];
  const auto & dNB_dX = _grad_phi[_j][_qp];
  const auto & NB = _phi[_j][_qp];
  const auto & i = comp_i;
  const auto & k = comp_k;
  
  const auto & P = _P[_qp];
  const auto & dP_dF = _dP_dF[_qp];
  const auto & kappa = _kappa;
  
  
  const auto & F = _F[_qp];
  const auto & F_inv = F.inverse();
  const auto & Jac = F.det();




  Real dResidual_Ai_dNodeDisplacement_Bk = 0.0;
  
  for (int J = 0; J < _ndisp; J++)
  {
    for (int L = 0; L < _ndisp; L++)
	{
      // No incompressibility enforced
	  // dResidual_Ai_dNodeDisplacement_Bk += dNA_dX(J) * dP_dF(i, J, k, L) * dNB_dX(L);
	
	
	
	  // Incompressibility ln(J)
	  auto term2 = (   dP_dF(i, J, k, L)   +   (kappa * F_inv(J, i) * F_inv(L, k))   -   (kappa * std::log(Jac) * F_inv(J, k) * F_inv(L, i))   );
	  
	  dResidual_Ai_dNodeDisplacement_Bk += dNB_dX(L) * term2 * dNA_dX(J);
	  
	}
  }



  return dResidual_Ai_dNodeDisplacement_Bk;
}