#include "purpleApp.h"
#include "Moose.h"
#include "AppFactory.h"
#include "ModulesApp.h"
#include "MooseSyntax.h"

InputParameters
purpleApp::validParams()
{
  InputParameters params = MooseApp::validParams();
  params.set<bool>("use_legacy_material_output") = false;
  return params;
}

purpleApp::purpleApp(InputParameters parameters) : MooseApp(parameters)
{
  purpleApp::registerAll(_factory, _action_factory, _syntax);
}

purpleApp::~purpleApp() {}

void 
purpleApp::registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  ModulesApp::registerAllObjects<purpleApp>(f, af, s);
  Registry::registerObjectsTo(f, {"purpleApp"});
  Registry::registerActionsTo(af, {"purpleApp"});

  /* register custom execute flags, action syntax, etc. here */
}

void
purpleApp::registerApps()
{
  registerApp(purpleApp);
}

/***************************************************************************************************
 *********************** Dynamic Library Entry Points - DO NOT MODIFY ******************************
 **************************************************************************************************/
extern "C" void
purpleApp__registerAll(Factory & f, ActionFactory & af, Syntax & s)
{
  purpleApp::registerAll(f, af, s);
}
extern "C" void
purpleApp__registerApps()
{
  purpleApp::registerApps();
}
