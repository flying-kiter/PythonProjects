import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm

class EHA(object):
    def __init__(self, sideNum, areaValue, height,turnsAx,turnsMx,\
                 pitchAx,pitchMx,IAx,IMx):
        """
        前后各有两个下划线
        """
        self.__sideNum = sideNum      # 定义n边形
        self.__areaValue = areaValue  # 定义n边形的截面面积,单位m^2
        self.__height =height         # 定义n边形柱状体的高度，单位m
        self.__turnsAx = turnsAx      # 定义侧面辅助线圈的匝数
        self.__turnsMx = turnsMx      # 定义平面主线圈的匝数
        self.__pitchAx = pitchAx      # 定义侧面辅助线圈的匝间距，单位m
        self.__pitchMx = pitchMx      # 定义平面主线圈的匝间距，单位m
        self.__IAx = IAx              # 定义侧面辅助线圈的电流激励，单位A
        self.__IMx = IMx              # 定义平面主线圈的电流激励，单位A
        self.__beta = 2*np.pi/sideNum #计算正n边形的边对应的外接圆圆心角
        self.__r = np.sqrt(2*areaValue/(sideNum*np.sin(self.__beta))) #计算正n边形的边对应的外接圆半径
        self.__w = 2*self.__r*np.sin(self.__beta/2) #计算正n边形的边长
        self.__ptNum = 200            #线段n等分
    """
    定义全局变量
    """
    u = 4*np.pi*(1e-7)    #真空磁导率
    i = 0     #计算n边形柱状体的第i个面（1,2,……,n）
    j = 0     #第i个面上从外向内的第j圈线圈（1,2,……,turnsAx）

    '''
    定义空间平面: y=x*tan(theta)
    '''
    def pt(self, theta):
        if(theta==np.pi/2 or theta == 3*np.pi/2): # tan(pi/2)与tan(3*pi/2)无穷大，单独讨论
            py = np.linspace((-1)*self.__r+self.__r/100, self.__r-self.__r/100, self.__ptNum) # The y-coordinate value of the sample points in the space.
            px = np.zeros(len(py)**2)
            pz = np.linspace((-1)*self.__r+self.__r/100, self.__r-self.__r/100, self.__ptNum) # The z-coordinate value of the sample points in the space.
            y_array = np.repeat(py,len(pz))
            z_array = np.tile(pz,len(py))
            py = y_array
            pz = z_array
            # The coordinate value of the sample points in the space.
            pt = np.array([px,py,pz])
            # print(pt)
            return pt 
        else:
            px = np.linspace((-1)*self.__r+self.__r/100, self.__r-self.__r/100, self.__ptNum)
            pz = np.linspace((-1)*self.__height+self.__height/100, self.__height-self.__height/100, self.__ptNum)
            fig_px = np.repeat(px,len(pz))
            fig_pz = np.tile(pz,len(px))
            px = fig_px
            py = fig_px*np.tan(theta)
            pz = fig_pz
            pt = np.array([px,py,pz])
            # print(pt)
            return pt 
    '''
    定义积分函数
    '''

    # 定义侧面线圈电流微元产生z轴方向的静磁场
    # 磁感应强度BZ_AX的待积函数，分上空间（增强）和下空间（削弱）
    # 两种函数: f_high, f_low
    def f_high(self,I,i,j,theta,pt):
        # I:流经该电流元的电流强度（A0）
        # i:该电流元位于正n边形的第i个侧面上
        # j:该电流元位于正n边形的第i个侧面,从外向内第j圈线圈上, 位于空间上区域
        # theta: 柱坐标系下，该电流元的旋转角(0,2*np.pi)
        # pt: 待计算的空间平面点集，默认200x200
        return (-1)*(EHA.u*I/4/np.pi)*((pt[1]-self.__r*np.cos(self.__beta/2)*np.sin(theta)/np.cos((i-1/2)*self.__beta-theta))*np.sin((i-1/2)*self.__beta)\
                                       +(pt[0]-self.__r*np.cos(self.__beta/2)*np.cos(theta)/np.cos((i-1/2)*self.__beta-theta))*np.cos((i-1/2)*self.__beta))\
                                       *(self.__r*np.cos(self.__beta/2))/(np.cos((i-1/2)*self.__beta-theta))**2\
                                        /np.power(((pt[0]-self.__r*np.cos(self.__beta/2)*np.cos(theta)/np.cos((i-1/2)*self.__beta-theta))**2\
                                                 +(pt[1]-self.__r*np.cos(self.__beta/2)*np.sin(theta)/np.cos((i-1/2)*self.__beta-theta))**2\
                                                 +(pt[2]-(self.__height/2-(j-1)*self.__pitchAx))**2),3/2)
    
    def f_low(self,I,i,j,theta,pt):
        # I:流经该电流元的电流强度（A0）
        # i:该电流元位于正n边形的第i个侧面上
        # j:该电流元位于正n边形的第i个侧面,从外向内第j圈线圈上，位于空间下区域，电流方向与f_high相反
        # theta: 柱坐标系下，该电流元的旋转角(0,2*np.pi)
        # pt: 待计算的空间平面点集，默认200x200
        return (EHA.u*I/4/np.pi)*((pt[1]-self.__r*np.cos(self.__beta/2)*np.sin(theta)/np.cos((i-1/2)*self.__beta-theta))*np.sin((i-1/2)*self.__beta)\
                                       +(pt[0]-self.__r*np.cos(self.__beta/2)*np.cos(theta)/np.cos((i-1/2)*self.__beta-theta))*np.cos((i-1/2)*self.__beta))\
                                       *(self.__r*np.cos(self.__beta/2))/(np.cos((i-1/2)*self.__beta-theta))**2\
                                        /np.power(((pt[0]-self.__r*np.cos(self.__beta/2)*np.cos(theta)/np.cos((i-1/2)*self.__beta-theta))**2\
                                                 +(pt[1]-self.__r*np.cos(self.__beta/2)*np.sin(theta)/np.cos((i-1/2)*self.__beta-theta))**2\
                                                 +(pt[2]-(-self.__height/2+(j-1)*self.__pitchAx))**2),3/2)

    def f_mid(self,I,i,j,theta,pt):
        # I:流经该电流元的电流强度（A）
        # i:该电流元位于正n边形的第i条边上
        # j:该电流元位于正n边形的第i条边,从外向内第j圈线圈上，位于中间平面Z=0
        # theta: 柱坐标系下，该电流元的旋转角(0,2*np.pi)
        # pt: 待计算的空间平面点集，默认200x200
        r = self.__r - (j-1)*self.__pitchMx/np.cos(self.__beta/2)
        return (-1)*(EHA.u*I/4/np.pi)*((pt[1]-r*np.cos(self.__beta/2)*np.sin(theta)/np.cos((i-1/2)*self.__beta-theta))*np.sin((i-1/2)*self.__beta)\
                                       +(pt[0]-r*np.cos(self.__beta/2)*np.cos(theta)/np.cos((i-1/2)*self.__beta-theta))*np.cos((i-1/2)*self.__beta))\
                                       *(r*np.cos(self.__beta/2))/(np.cos((i-1/2)*self.__beta-theta))**2\
                                        /np.power(((pt[0]-r*np.cos(self.__beta/2)*np.cos(theta)/np.cos((i-1/2)*self.__beta-theta))**2\
                                                 +(pt[1]-r*np.cos(self.__beta/2)*np.sin(theta)/np.cos((i-1/2)*self.__beta-theta))**2\
                                                 +(pt[2])**2),3/2)



    # 定义侧面线圈单根电流导线产生z轴方向的静磁场
    # 磁感应强度BZ_AX的积分值，分上空间（增强）和下空间（削弱）
    # 两种函数: IntegrateSingleWireHigh, IntegrateSingleWireLow
    # 积分公式：复合Simpson公式
    def IntegrateSingleWireHigh(self,I,i,j,pt):
        # I:流经该电流元的电流强度（A0）
        # i:该电流元位于正n边形的第i个侧面上
        # j:该电流元位于正n边形的第i个侧面,从外向内第j圈线圈上，位于空间下区域，电流方向与f_high相反
        # theta: 柱坐标系下，该电流元的旋转角(0,2*np.pi)
        # pt: 待计算的空间平面点集，默认200x200
        # 本函数将一根电流线划分为均长的50段，采用复合积分：Simpson公式法进行计算
        HalfDeltaTheta = np.arctan((self.__w/2-(j-1)*self.__pitchAx)/(self.__r*np.cos(self.__beta/2)-(j-1)*self.__pitchAx))
        ThetaValueSet = np.linspace(((i-1/2)*self.__beta-HalfDeltaTheta),\
                                    ((i-1/2)*self.__beta+HalfDeltaTheta),\
                                    101)
        FuncValueSet = (self.f_high(I,i,j,ThetaValueSet[0],pt)).reshape(self.__ptNum**2,1)
        temp = 0
        for i in range(100):
            temp = self.f_high(I,i,j,ThetaValueSet[i+1],pt)
            temp = temp.reshape(len(temp),1)
            FuncValueSet = np.hstack((FuncValueSet, temp))

        h = 2*HalfDeltaTheta/50
        weight = [h/6]
        for i in range(99):
            if((i+1)%2 == 1):
                weight.append(2*h/3)
            else:
                weight.append(h/3)
        weight.append(h/6)
        weight = np.array(weight)
        weight = np.tile(weight, self.__ptNum**2)
        weight = weight.reshape(self.__ptNum**2,101)
        assert len(weight) == len(FuncValueSet)
        assert len(weight[0]) == len(FuncValueSet[0])
        IntegratedResult = FuncValueSet * weight
        IntegratedResult = np.sum(IntegratedResult,axis=1)
        return IntegratedResult

    # 定义侧面线圈单根电流导线产生z轴方向的静磁场
    # 磁感应强度BZ_AX的积分值，分上空间（增强）和下空间（削弱）
    # 两种函数: IntegrateSingleWireHigh, IntegrateSingleWireLow
    # 积分公式：复合Simpson公式
    def IntegrateSingleWireLow(self,I,i,j,pt):
        # I:流经该电流元的电流强度（A0）
        # i:该电流元位于正n边形的第i个侧面上
        # j:该电流元位于正n边形的第i个侧面,从外向内第j圈线圈上，位于空间下区域，电流方向与f_high相反
        # theta: 柱坐标系下，该电流元的旋转角(0,2*np.pi)
        # pt: 待计算的空间平面点集，默认200x200
        # 本函数将一根电流线划分为均长的50段，采用复合积分：Simpson公式法进行计算
        HalfDeltaTheta = np.arctan((self.__w/2-(j-1)*self.__pitchAx)/(self.__r*np.cos(self.__beta/2)-(j-1)*self.__pitchAx))
        ThetaValueSet = np.linspace(((i-1/2)*self.__beta-HalfDeltaTheta),\
                                    ((i-1/2)*self.__beta+HalfDeltaTheta),\
                                    101)
        FuncValueSet = (self.f_low(I,i,j,ThetaValueSet[0],pt)).reshape(self.__ptNum**2,1)
        temp = 0
        for i in range(100):
            temp = self.f_low(I,i,j,ThetaValueSet[i+1],pt)
            temp = temp.reshape(len(temp),1)
            FuncValueSet = np.hstack((FuncValueSet, temp))

        h = 2*HalfDeltaTheta/50
        weight = [h/6]
        for i in range(99):
            if((i+1)%2 == 1):
                weight.append(2*h/3)
            else:
                weight.append(h/3)
        weight.append(h/6)
        weight = np.array(weight)
        weight = np.tile(weight, self.__ptNum**2)
        weight = weight.reshape(self.__ptNum**2,101)
        assert len(weight) == len(FuncValueSet)
        assert len(weight[0]) == len(FuncValueSet[0])
        IntegratedResult = FuncValueSet * weight
        IntegratedResult = np.sum(IntegratedResult,axis=1)
        return IntegratedResult
    
    # 定义主平面线圈的单根电流导线产生z轴方向的静磁场
    # 磁感应强度BZ_AX的积分值
    # 积分公式：复合Simpson公式
    def IntegrateSingleWireMid(self,I,i,j,pt):
        ThetaValueSet = np.linspace((i-1)*self.__beta, i*self.__beta, 101)
        FuncValueSet = (self.f_mid(I,i,j,ThetaValueSet[0],pt)).reshape(self.__ptNum**2,1)
        temp = 0
        for i in range(100):
            temp = self.f_mid(I,i,j,ThetaValueSet[i+1],pt)
            temp = temp.reshape(len(temp),1)
            FuncValueSet = np.hstack((FuncValueSet, temp))

        h = self.__beta/50
        weight = [h/6]
        for i in range(99):
            if((i+1)%2 == 1):
                weight.append(2*h/3)
            else:
                weight.append(h/3)
        weight.append(h/6)
        weight = np.array(weight)
        weight = np.tile(weight, self.__ptNum**2)
        weight = weight.reshape(self.__ptNum**2,101)
        assert len(weight) == len(FuncValueSet)
        assert len(weight[0]) == len(FuncValueSet[0])
        IntegratedResult = FuncValueSet * weight
        IntegratedResult = np.sum(IntegratedResult,axis=1)
        return IntegratedResult

    
    # 定义侧面所有线圈的电流导线产生z轴方向的静磁场
    # 磁感应强度BZ_AX的积分值，分上空间导线积分（增强）和下空间导线积分（削弱）
    # 两种函数: IntegrateWiresHigh, IntegrateWiresLow
    # 积分公式：复合Simpson公式
    def IntegrateWiresHigh(self,I,pt):
        # I:流经该电流元的电流强度（A0）
        # i:该电流元位于正n边形的第i个侧面上
        # j:该电流元位于正n边形的第i个侧面,从外向内第j圈线圈上，位于空间下区域，电流方向与f_high相反
        # theta: 柱坐标系下，该电流元的旋转角(0,2*np.pi)
        # pt: 待计算的空间平面点集，默认200x200
        # 本函数将一根电流线划分为均长的50段，采用复合积分：Simpson公式法进行计算
        result = 0
        for num_side in range(self.__sideNum):
            for num_loop in range(self.__turnsAx):
                result += self.IntegrateSingleWireHigh(I,num_side+1,num_loop+1,pt)
        return result
    
    # 定义侧面所有线圈的电流导线产生z轴方向的静磁场
    # 磁感应强度BZ_AX的积分值，分上空间导线积分（增强）和下空间导线积分（削弱）
    # 两种函数: IntegrateWiresHigh, IntegrateWiresLow
    # 积分公式：复合Simpson公式
    def IntegrateWiresLow(self,I,pt):
        # I:流经该电流元的电流强度（A0）
        # i:该电流元位于正n边形的第i个侧面上
        # j:该电流元位于正n边形的第i个侧面,从外向内第j圈线圈上，位于空间下区域，电流方向与f_high相反
        # theta: 柱坐标系下，该电流元的旋转角(0,2*np.pi)
        # pt: 待计算的空间平面点集，默认200x200
        # 本函数将一根电流线划分为均长的50段，采用复合积分：Simpson公式法进行计算
        result = 0
        for num_side in range(self.__sideNum):
            for num_loop in range(self.__turnsAx):
                result += self.IntegrateSingleWireLow(I,num_side+1,num_loop+1,pt)
        return result
    
    # 定义主平面线圈的电流导线产生z轴方向的静磁场
    # 磁感应强度BZ_AX的积分值
    # 积分公式：复合Simpson公式
    def IntegrateWiresMid(self, I, pt):
        result = 0
        for num_side in range(self.__sideNum):
            for num_loop in range(self.__turnsMx):
                result += self.IntegrateSingleWireMid(I,num_side+1,num_loop+1,pt)
        return result
    
    '''
    综合侧面辅助线圈与主平面线圈的积分，全部积分之和即为所求数据
    '''
    def PlaneTheta(self, theta):
        pt = self.pt(theta)
        return self.IntegrateWiresHigh(self.__IAx, pt)+\
               self.IntegrateWiresLow(self.__IAx, pt)+\
               self.IntegrateWiresMid(self.__IMx, pt)
    '''
    可视化数据, 以平面x=0为基准平面, 求基准平面绕z轴逆时针旋转theta角度(弧度制)后, 
    平面上的磁感应强度(z轴方向分量)分布图
    '''
    def ShowPlaneTheta(self, theta):
        pt = self.pt(theta)
        BZ = self.PlaneTheta(theta)
        plt.figure(figsize=(8, 6))
        lvls = np.linspace(-2e-4,2e-4,100)
        cp = plt.contourf(pt[0].reshape((self.__ptNum,self.__ptNum))/np.cos(theta), pt[2].reshape((self.__ptNum,self.__ptNum)), BZ.reshape((self.__ptNum,self.__ptNum)), levels=lvls, cmap=cm.jet)
        # 添加颜色条
        plt.colorbar(cp)

        # 设置图表标题和坐标轴标签
        plt.title('Fluxdensity in the z-axis direction, offset angle {}rad\nMax{},Min{}'.format(theta,np.max(BZ),np.min(BZ)))
        plt.xlabel('horiziontal-axis')
        plt.ylabel('z-axis')

        # 显示图表
        plt.show()

    ## 计算并展示平面Z = z上的Bz值
    def PlaneZ(self, z):
        px = np.linspace((-1)*self.__r+self.__r/100, self.__r-self.__r/100, self.__ptNum)
        py = np.linspace((-1)*self.__r+self.__r/100, self.__r-self.__r/100, self.__ptNum)
        pz = z*np.ones(self.__ptNum**2)
        xarray = np.repeat(px,self.__ptNum)
        yarray = np.tile(py, self.__ptNum)
        pt = np.array((xarray,yarray,pz))
        return self.IntegrateWiresHigh(self.__IAx, pt)+\
               self.IntegrateWiresLow(self.__IAx, pt)+\
               self.IntegrateWiresMid(self.__IMx, pt)
        
    def ShowPlaneZ(self, z):
        px = np.linspace((-1)*self.__r+self.__r/100, self.__r-self.__r/100, self.__ptNum)
        py = np.linspace((-1)*self.__r+self.__r/100, self.__r-self.__r/100, self.__ptNum)
        pz = z*np.ones(self.__ptNum**2)
        xarray = np.repeat(px,self.__ptNum)
        yarray = np.tile(py, self.__ptNum)
        pt = np.array((xarray,yarray,pz))
        BZ = self.PlaneZ(z)
        plt.figure(figsize=(8, 6))
        lvls = np.linspace(-8e-5,2e-4,100)
        cp = plt.contourf(pt[0].reshape((self.__ptNum,self.__ptNum)), pt[1].reshape((self.__ptNum,self.__ptNum)), BZ.reshape((self.__ptNum,self.__ptNum)), levels=lvls, cmap=cm.jet)
        # 添加颜色条
        plt.colorbar(cp)

        # 设置图表标题和坐标轴标签
        plt.title('Fluxdensity in the z-axis plane:z={}m\nMax{},Min{}'.format(z,np.max(BZ),np.min(BZ)))
        plt.xlabel('x-axis')
        plt.ylabel('y-axis')

        # 显示图表
        plt.show()

    """
    the function to display the parameters
    """
    def PrintParameters(self):
        print("sideNum = {}".format(self.__sideNum))
        print("areaValue = {}m^2".format(self.__areaValue))
        print("height = {}m".format(self.__height))
        print("turnsAx = {}".format(self.__turnsAx))
        print("turnsMx = {}".format(self.__turnsMx))
        print("pitchAx = {}m".format(self.__pitchAx))
        print("pitchMx = {}m".format(self.__pitchMx))
        print("IAx = {}A".format(self.__IAx))
        print("IMx = {}A".format(self.__IMx))
        print("Beta = {}RAD".format(self.__beta))
        print("r = {}m".format(self.__r))
        print("w = {}m".format(self.__w))
        
        """
        the functions to update the parameters, ready for optimization
        """
    def UpdateSideNum(self,newSideNum):
        self.__sideNum = newSideNum
        self.__beta = 2*np.pi/self.__sideNum #计算正n边形的边对应的外接圆圆心角
        self.__r = np.sqrt(2*self.__areaValue/(self.__sideNum*np.sin(self.__beta))) #计算正n边形的边对应的外接圆半径
        self.__w = 2*self.__r*np.sin(self.__beta/2) #计算正n边形的边长
    def UpdateAreaValue(self,newAreaValue):
        self.__areaValue = newAreaValue
        self.__r = np.sqrt(2*self.__areaValue/(self.__sideNum*np.sin(self.__beta))) #计算正n边形的边对应的外接圆半径
        self.__w = 2*self.__r*np.sin(self.__beta/2) #计算正n边形的边长
    def UpdateHeight(self,newHeight):
        self.__height = newHeight
    def UpdateTurnsAx(self,newTurnsAx):
        self.__turnsAx = newTurnsAx
    def UpdateTurnsMx(self,newTurnsMx):
        self.__turnsMx = newTurnsMx
    def UpdatePitchAx(self,newPitchAx):
        self.__pitchAx = newPitchAx
    def UpdatePitchMx(self,newPitchMx):
        self.__pitchMx = newPitchMx
    def UpdateIAx(self, newIAx):
        self.__IAx = newIAx
    def UpdateIMx(self, newIMx):
        self.__IMx = newIMx
    def Update(self,newSideNum, newAreaValue, newHeight, newTurnsAx\
               , newTurnsMx, newPitchAx, newPitchMx, newIAx, newIMx):
        self.UpdateSideNum(newSideNum)
        self.UpdateAreaValue(newAreaValue)
        self.UpdateHeight(newHeight)
        self.UpdateTurnsAx(newTurnsAx)
        self.UpdateTurnsMx(newTurnsMx)
        self.UpdatePitchAx(newPitchAx)
        self.UpdatePitchMx(newPitchMx)
        self.UpdateIAx(newIAx)
        self.UpdateIMx(newIMx)

    #利用正多边形的对称性，在截面Z=z上的EHA内部磁场可以平均分成n等份，
    #这里只需要计算一份即可，即theta∈(0, beta)
    def AverageFluxDensityAtZ(self,z):
        theta = np.linspace(0,self.__beta,self.__ptNum) # beta角被均分为200份（默认self.__ptNum = 200）
        deltaTheta = self.__beta/self.__ptNum
        r_max = self.__r*np.cos(self.__beta/2)/np.cos(self.__beta/2-theta) #每个theta角上的线段被均分为200份（默认self.__ptNum = 200）
        deltaR = (r_max/self.__ptNum).repeat(self.__ptNum)
        theta = theta.repeat(self.__ptNum)
        r = np.linspace(0,r_max,self.__ptNum)
        r = r.reshape(-1).tolist()
        assert len(theta) == len(r)
        # 定义目标截面上的空间点集，默认（200*200）
        px = r*np.cos(theta)
        py = r*np.sin(theta)
        pz = z*np.ones(self.__ptNum**2)
        pt = np.array((px,py,pz))

        assert len(deltaR) == len(r)
        deltaS = r*deltaR*deltaTheta
        Bz =  self.IntegrateWiresHigh(self.__IAx, pt)+\
              self.IntegrateWiresLow(self.__IAx, pt)+\
              self.IntegrateWiresMid(self.__IMx, pt)
        assert len(deltaS) == len(Bz)
        Flux = np.sum(Bz*deltaS)
        S = 1/2 * self.__r**2 *np.sin(self.__beta)
        AverageFluxDensity = Flux / S
        return AverageFluxDensity

    def FluxDensityStandardDeviaton(self):
        z = np.linspace(0.001,self.__height/2-0.001,10)
        result = []
        for i in z:
            result.append(self.AverageFluxDensityAtZ(i))
        result = np.array(result)
        return np.std(result)
    
    # 优化电流分配，I = IMx/IAx
    def OptimizeCurrentRatio(self):
        I = np.linspace(0.5,2,10)
        stdSet = []
        for i in range(len(I)):
            self.UpdateIMx(I[i])
            stdSet.append(self.FluxDensityStandardDeviaton())
        min_index = np.argmin(stdSet)
        self.UpdateIMx(I[min_index])
        return I[min_index]
    
    ####################################################################################################
    ####################################################################################################
    # 以下优化函数默认EHA的初始设置为sideNum = 4, areaValue = 0.0025, height = 0.05, turnsAx = 6, 
    # turnsMx = 5, pitchAx = 0.003, pitchMx = 0.002, IAx = 1, IMx = 1
    ####################################################################################################
    ####################################################################################################
    # 优化侧面线圈匝数
    def OptimizeTurnsAx(self):
        stdSet = []
        for turnsAx in range(8):
            self.UpdateTurnsAx(turnsAx)
            stdSet.append(self.FluxDensityStandardDeviaton())
        min_index = np.argmin(stdSet)
        self.UpdateTurnsAx(min_index+1)
        return min_index+1
    
    # 优化平面主线圈匝数
    def OptimizeTurnsMx(self):
        stdSet = []
        for turnsMx in range(8):
            self.UpdateTurnsMx(turnsMx)
            stdSet.append(self.FluxDensityStandardDeviaton())
        min_index = np.argmin(stdSet)
        self.UpdateTurnsMx(min_index+1)
        return min_index+1

    # 优化侧面线圈匝间距
    def OptimizePitchAx(self):
        stdSet = []
        pitchSet = np.array((0.001,0.002,0.003,0.004))
        for pitchAx in pitchSet:
            self.UpdatePitchAx(pitchAx)
            stdSet.append(self.FluxDensityStandardDeviaton())
        min_index = np.argmin(stdSet)
        self.UpdatePitchAx(pitchSet[min_index])
        return pitchSet[min_index]
    
    # 优化平面主线圈匝间距
    def OptimizePitchMx(self):
        stdSet = []
        eleMax = int(np.sqrt(2*self.__areaValue/self.__sideNum/np.sin(self.__beta))*np.cos(self.__beta/2)/4)*1000
        pitchSet = np.linspace(0.001,0.001*eleMax,eleMax)
        for pitchMx in pitchSet:
            self.UpdatePitchMx(pitchMx)
            stdSet.append(self.FluxDensityStandardDeviaton())
        min_index = np.argmin(stdSet)
        self.UpdatePitchMx(pitchSet[min_index])
        return pitchSet[min_index]
    
    def Optimize(self):
        optimizedCurrentRatio = self.OptimizeCurrentRatio()
        optimizedTurnsAx = self.OptimizeTurnsAx()
        optimizedTurnsMx = self.OptimizeTurnsMx()
        optimizedPitchAx = self.OptimizePitchAx()
        optimizedPitchMx = self.OptimizePitchMx()
        stdSet = []
        index = []
        temp = np.array((-1,0,1))
        for turnsAx in temp:
            for turnsMx in temp:
                self.UpdateTurnsAx(self.__turnsAx+turnsAx)
                self.UpdateTurnsMx(self.__turnsMx+turnsMx)
                stdSet.append(self.FluxDensityStandardDeviaton())
                index.append([turnsAx,turnsMx])
        min_index = np.argmin(stdSet)
        self.UpdateTurnsAx(self.__turnsAx + index[min_index][0])
        self.UpdateTurnsMx(self.__turnsMx + index[min_index][1])
        self.PrintParameters()

# 创建测试对象
t = EHA(sideNum = 4, areaValue = 0.0025, height = 0.05, turnsAx = 6, turnsMx = 5, pitchAx = 0.003, pitchMx = 0.002, IAx = 1, IMx = 1)
print(t.StandardDeviaton())
