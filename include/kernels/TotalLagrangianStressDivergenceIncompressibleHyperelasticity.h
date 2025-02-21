#pragma once

#include "TotalLagrangianStressDivergenceBase.h"
#include "GradientOperator.h"

/// Custom kernel enforcing stress equilibrium with pressure dependency
///
/// Implements a total Lagrangian formulation where the First Piola-Kirchhoff (PK1)
/// stress depends on both the deformation gradient \( F \) and a coupled pressure
/// variable \( p \).
///
/// This kernel computes:
/// - Residual: \(\frac{\partial v_{\alpha}}{\partial X_J} P_{\alpha J}\),
/// - Displacement Jacobian: \(\frac{\partial P_{\alpha J}}{\partial F_{kL}}\),
/// - Off-diagonal pressure Jacobian: \(\frac{\partial P_{\alpha J}}{\partial p}\).
template <class G>
class TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase : public TotalLagrangianStressDivergenceBase<G>
{
public:
  static InputParameters validParams();
  TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase(const InputParameters & parameters);
  
  virtual void initialSetup() override;

protected:
  /// Computes the residual contribution for stress equilibrium
  virtual Real computeQpResidual() override;

  /// Computes the diagonal Jacobian contribution (displacement terms)
  virtual Real computeQpJacobian() override;

  /// Computes the off-diagonal Jacobian contribution (pressure coupling)
  virtual Real computeQpOffDiagJacobian(unsigned int jvar) override;

  /// Material parameter (shear modulus)
  const Real _mu;

  /// Coupled pressure variable index
  const unsigned int _p_var;

  /// Coupled pressure field at quadrature points
  const VariableValue & _p;
};

/// Enforce equilibrium with a total Lagrangian formulation in Cartesian coordinates.
typedef TotalLagrangianStressDivergenceIncompressibleHyperelasticityBase<GradientOperatorCartesian>
    TotalLagrangianStressDivergenceIncompressibleHyperelasticity;
