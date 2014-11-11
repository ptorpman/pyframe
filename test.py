
if __name__ == '__main__':

    Registrar().CoRegisterClassObject('123', TestFactory())

    try:
        Registrar().CoRegisterClassObject('123', TestFactory())
    except Exception as exc:
        print "Got expected exception"

    clsobj = Registrar().CoGetClassObject('123', IClassFactory.IID_IClassFactory())
    print clsobj

    inst1 = clsobj.CreateInstance('001')
    inst2 = clsobj.CreateInstance('002')
    
    iunk = inst1.QueryInterface(IUnknown.IID_IUnknown())
    itest = inst1.QueryInterface(ITest.IID_ITest())
    iunk.Release(IUnknown.IID_IUnknown())
    itest.test_me()

    try:
        inst1.Release(ITest.IID_ITest())
    except NoReferencesException as exc:
        print "Time to remove instance"
        del inst1
