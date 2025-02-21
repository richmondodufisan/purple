/// Custom kernel enforcing stress equilibrium with pressure dependency
///
/// Implements a total Lagrangian formulation where the First Piola-Kirchhoff (PK1)
/// stress depends on both the deformation gradient \( F \) and a coupled pressure
/// variable \( p \).





#pragma once

#include "LagrangianStressDivergenceBase.h"
#include "GradientOperator.h"



/////////////////// MOOSE STUFF /////////////////////////////
template <class G>
class TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase : public LagrangianStressDivergenceBase, public G
{
public:  
  static InputParameters baseParams()
  {
    InputParameters params = LagrangianStressDivergenceBase::validParams();
    return params;
  }
  static InputParameters validParams();
  TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase(const InputParameters & parameters);
  
  virtual void initialSetup() override;

protected:
  virtual RankTwoTensor gradTest(unsigned int component) override;
  virtual RankTwoTensor gradTrial(unsigned int component) override;

  virtual Real computeQpResidual() override;
  virtual Real computeQpJacobian() override;
  virtual Real computeQpOffDiagJacobian(unsigned int jvar) override;
  
  
  
  
  

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ///////////////////////////////////////////////////////IRRELEVANT, ignore //////////////////////////////////////////////////////////////////////
  virtual void precalculateJacobianDisplacement(unsigned int component) override;
  virtual Real computeQpJacobianDisplacement(unsigned int alpha, unsigned int beta) override;
  virtual Real computeQpJacobianTemperature(unsigned int cvar) override;
  virtual Real computeQpJacobianOutOfPlaneStrain() override;

  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  
  
  
  /// The 1st Piola-Kirchhoff stress
  const MaterialProperty<RankTwoTensor> & _pk1;

  /// The derivative of the PK1 stress with respect to the
  /// deformation gradient
  const MaterialProperty<RankFourTensor> & _dpk1;
  
  
  
  ////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  // Material parameter (shear modulus)
  const Real _mu;

  /// Coupled pressure variable index
  const unsigned int _p_var;

  /// Coupled pressure field at quadrature points
  const VariableValue & _p;
  
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  
  
  
  
  
  

private:
  /// The unstabilized trial function gradient
  virtual RankTwoTensor gradTrialUnstabilized(unsigned int component);

  /// The stabilized trial function gradient
  virtual RankTwoTensor gradTrialStabilized(unsigned int component);
  
};  
  
  
  
  
  
  
template <>
inline InputParameters
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>::validParams()
{
  InputParameters params = TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase::baseParams();
  
  // This kernel requires use_displaced_mesh to be off
  params.suppressParameter<bool>("use_displaced_mesh");
  
  
  
  
  
  ////////////////////////// ADDED STUFF ////////////////////////////////////////////////////////////////////////////////////////////////////////
  params.addClassDescription("Enforce equilibrium with a total Lagrangian formulation in Cartesian coordinates.");
  params.addRequiredParam<Real>("mu", "Shear modulus");
  params.addRequiredCoupledVar("pressure", "Pressure variable (coupled)");
  ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  
  
  
  
  
  return params;
}

template <>
inline void
TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>::initialSetup()
{
  if (getBlockCoordSystem() != Moose::COORD_XYZ)
    mooseError("This kernel should only act in Cartesian coordinates.");
}

typedef TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>
    TotalLagrangianStressDivergenceIncompressibleHyperelasticity;

