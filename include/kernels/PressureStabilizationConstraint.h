#pragma once

#include "ADKernel.h"
#include "DerivativeMaterialInterface.h"
#include "RankTwoTensor.h"
#include "RankFourTensor.h"
#include "RankTwoTensor.h"
#include "Eigen/Core"
#include "Eigen/Dense"
#include <unsupported/Eigen/CXX11/Tensor>

class PressureStabilizationConstraint : public DerivativeMaterialInterface<ADKernel>
{
  public:
    static InputParameters validParams();
    PressureStabilizationConstraint(const InputParameters & parameters);

  protected:
    virtual ADReal computeQpResidual() override;

    /// Base name of the material system that this kernel applies to
    const std::string _base_name;

	const VariableValue & _pressure;
};


