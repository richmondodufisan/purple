#include "TLStressDivergence.h"
#include "DerivativeMaterialInterface.h"

registerMooseObject("purpleApp", TLStressDivergence);

InputParameters
TLStressDivergence::validParams()
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
  // params.addClassDescription("Enforce equilibrium with a total Lagrangian formulation in Cartesian coordinates.");
  // params.addRequiredParam<Real>("mu", "Shear modulus");
  // params.addRequiredCoupledVar("pressure", "Pressure variable (coupled)");
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

  return params;
}

TLStressDivergence::TLStressDivergence(const InputParameters & parameters)
  : DerivativeMaterialInterface<Kernel>(parameters),
  
  
    _base_name(isParamValid("base_name") ? getParam<std::string>("base_name") + "_" : ""),
	
	
	
    _P(getMaterialPropertyByName<RankTwoTensor>(_base_name + "pk1_stress")),
    _dP_dF(getMaterialPropertyByName<RankFourTensor>(_base_name + "pk1_jacobian")),
	_F(getMaterialPropertyByName<RankTwoTensor>(_base_name + "deformation_gradient")),



    _component(getParam<unsigned int>("component")),
    _ndisp(coupledComponents("displacements")),
    _disp_var(_ndisp)
	
	
	////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
	// _mu(getParam<Real>("mu")),    
    // _p_var(coupled("pressure")),           
    // _pressure(coupledValue("pressure"))    
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
TLStressDivergence::computeQpResidual()
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
  
  
  
  Real residual_i = 0.0;
  
  for (int J = 0;  J < _ndisp; ++J)
  {
    residual_i += P(i, J) * dNA_dX(J);
  }  



  return residual_i;
}

Real
TLStressDivergence::computeQpJacobian()
{
  const auto ivar = _var.number();

  for (unsigned int i = 0; i < _ndisp; ++i)
    if (ivar == _disp_var[i])
      return computeQpJacobianDisplacement(_component, _component);

  mooseError("Jacobian for unknown variable requested");
  return 0.0;
}

Real
TLStressDivergence::computeQpOffDiagJacobian(unsigned int jvar)
{
  for (unsigned int j = 0; j < _ndisp; ++j)
    if (jvar == _disp_var[j])
      return computeQpJacobianDisplacement(_component, j);

  // if (jvar == _p_var)
    // return computeQpJacobianPressure(_component);

  mooseError("Jacobian for unknown variable requested");
  return 0.0;
}

Real
TLStressDivergence::computeQpJacobianDisplacement(unsigned int comp_i, unsigned int comp_k)
{

  const auto & dNA_dX = _grad_test[_i][_qp];
  const auto & NA = _test[_i][_qp];
  const auto & dNB_dX = _grad_phi[_j][_qp];
  const auto & NB = _phi[_j][_qp];
  const auto & i = comp_i;
  const auto & k = comp_k;
  
  const auto & P = _P[_qp];
  const auto & dP_dF = _dP_dF[_qp];




  Real dResidual_Ai_dNodeDisplacement_Bk = 0.0;
  
  for (int J = 0; J < _ndisp; J++)
  {
    for (int L = 0; L < _ndisp; L++)
	{
      dResidual_Ai_dNodeDisplacement_Bk += dNA_dX(J) * dP_dF(i, J, k, L) * dNB_dX(L);
	}
  }



  return dResidual_Ai_dNodeDisplacement_Bk;
}




// Real
// TLStressDivergence::computeQpJacobianPressure(unsigned int comp_i)
// {
  
  // const auto & dNA_dX = _grad_test[_i][_qp];
  // const auto & NA = _test[_i][_qp]
  // const auto & NB = _phi[_j][_qp];
  // const auto & i = comp_i;
  
  // const auto & P = _P[_qp];
  // const auto & dP_dF = _dP_dF[_qp];
  
  // const auto & pressure = _pressure[_qp]
  // const auto & mu = _mu;

  // dResidual_Ai_dPressure = 0.0;

  // return dResidual_Ai_dPressure;
// }
