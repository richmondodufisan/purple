#pragma once

#include "Kernel.h"
#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>

class IncompressibilityConstraint : public DerivativeMaterialInterface<Kernel>
{
  public:
    static InputParameters validParams();
    IncompressibilityConstraint(const InputParameters & parameters);

  protected:
    virtual Real computeQpResidual() override;

    /// Base name of the material system that this kernel applies to
    const std::string _base_name;

	const MaterialProperty<RankTwoTensor> & _deformation_gradient;
};
